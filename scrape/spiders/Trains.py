import scrapy
import json
import urllib
from datetime import timedelta
from scrapy.exceptions import CloseSpider
import re
from ..items import Train, Record


class BaseSpider(scrapy.Spider):
	allowed_domains = ['12306.cn']
	start_urls = ['https://kyfw.12306.cn/otn/resources/js/query/train_list.js']
	date = None
	keys = None

	def pre_parse(self, body):
		if not self.date:
			from datetime import date
			self.date = date.today().isoformat()
		if isinstance(self.date, str) and self.date.isnumeric():
			from datetime import date
			date = date.today() + timedelta(days=int(self.date))
			self.date = date.isoformat()

		# Parse page info into JSON
		data = body.decode('utf-8')
		data = data[data.index('=') + 1:]  # REMOVE var train_list =
		jsonData = json.loads(data)
		if not jsonData:
			raise CloseSpider('Can not parse data as JSON')

		# Extract needed date
		jsonData = jsonData.get(self.date)
		if not jsonData:
			raise CloseSpider('Can not find designated date')

		# Set train parsing keys to all the keys by default
		if not self.keys:
			keys = jsonData.keys()

		# Extract useful records into a single list
		telecodes = {}
		for prefix in keys:
			contentInPrefix = jsonData.get(prefix)
			if not contentInPrefix:
				self.logger.warning('Train prefix %s not exist', prefix)
				continue
			for train in contentInPrefix:
				match = re.match(r'(\w+)\((.+)-(.+)\)', train['station_train_code'])
				if not match:
					self.logger.warning('Can not parse info str %s for train %s', train['station_train_code'], train['train_no'])
					continue
				name = match.group(1)
				telecode = train['train_no']
				if telecode in telecodes:
					telecodes[telecode].append(name)
				else:
					telecodes[telecode] = [name]
		return telecodes

	# Called when train list page was scraped.
	# Create trains and records for the selected day.
	def parse(self, response):
		content = self.pre_parse(response.body)
		for (telecode, names) in content.items():
			item = self.parseItem(telecode, names)
			if item:
				yield item


class TrainSpider(BaseSpider):
	name = 'Trains'

	def parseItem(self, telecode, names):
		train = Train(
			names=names,
			telecode=telecode
		)
		if train.duplicated:
			self.logger.debug('Duplicated Train %s will be discarded' % names)
		else:
			parameters = {
				'train_no': telecode,
				'from_station_telecode': 'ABC',
				'to_station_telecode': 'CBA',
				'depart_date': self.date,
			}
			url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?' + urllib.parse.urlencode(parameters)
			request = scrapy.Request(url, callback=self.parseSchedule)
			request.meta['train'] = train
			request.meta['dont_redirect'] = True
			return request

	def parseSchedule(self, response):
		jsonData = json.loads(response.body.decode('utf-8'))
		stops = []
		lastTime = timedelta()

		for stop in jsonData['data']['data']:
			# Parse time string into timedelta objects
			departureTime = re.match(r'(\d{2}):(\d{2})', stop['start_time'])
			departureTime = departureTime.groups() if departureTime else None
			arrivalTime = re.match(r'(\d{2}):(\d{2})', stop['arrive_time'])
			arrivalTime = arrivalTime.groups() if arrivalTime else None
			stopDict = {'station': stop['station_name']}
			if arrivalTime:
				arrivalTime = timedelta(hours=int(arrivalTime[0]), minutes=int(arrivalTime[1]))
				if lastTime > arrivalTime:  # Date interpretation
					arrivalTime += timedelta(days=1)
				lastTime = arrivalTime
				stopDict['arrivalTime'] = arrivalTime
			if departureTime:
				departureTime = timedelta(hours=int(departureTime[0]), minutes=int(departureTime[1]))
				if lastTime > departureTime:  # Date interpretation
					departureTime += timedelta(days=1)
				lastTime = departureTime
				stopDict['departureTime'] = departureTime

			stops.append(stopDict)

		if len(stops) is 0:
			self.logger.error("empty stops %s" % jsonData['data']['data'])
			return
		stops[0].pop('arrivalTime', None)
		stops[-1].pop('departureTime', None)
		train = response.meta['train']
		train['stops'] = stops
		train['since'] = self.date
		yield train


class RecordSpider(BaseSpider):
	name = 'Records'

	def parseItem(self, telecode, names):
		return Record(
			departureDate=self.date,
			telecode=telecode,
		)
