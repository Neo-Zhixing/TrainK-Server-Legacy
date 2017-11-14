import scrapy
import json
import urllib
from datetime import timedelta
from scrapy.exceptions import CloseSpider
import re
from scrape.items import Train, Record


class Spider(scrapy.Spider):
	name = 'Trains'
	allowed_domains = ['12306.cn']
	start_urls = ['https://kyfw.12306.cn/otn/resources/js/query/train_list.js']
	createRecords = False
	date = None
	keys = None

	def pre_parse(self, response):
		if not self.date:
			from datetime import date
			self.date = date.today().isoformat()

		# Parse page info into JSON
		data = response.body.decode('utf-8')
		data = data[data.index('=') + 1:]  # REMOVE var train_list =
		jsonData = json.loads(data)
		if not jsonData:
			return 'Can not parse data as JSON'

		# Extract needed date
		jsonData = jsonData.get(self.date)
		if not jsonData:
			return 'Can not find designated date'

		# Set train parsing keys to all the keys by default
		if not self.keys:
			keys = jsonData.keys()

		# Extract useful records into a single list
		content = []
		for prefix in keys:
			contentInPrefix = jsonData.get(prefix)
			if contentInPrefix:
				content.extend(contentInPrefix)
			else:
				self.logger.warning('Train prefix %s not exist', prefix)
				continue
		return content

	def parseRecords(self, content):
		for train in content:
				record = Record(
					departureDate=self.date,
					telecode=train['train_no'],
				)
				yield record

	def parseSchedules(self, content):
		for train in content:
			trainIDMatch = re.match(r'(\w+)\((.+)-(.+)\)', train['station_train_code'])
			telecode = train['train_no']
			name = trainIDMatch.group(1)
			if not name:
				self.logger.warning('Can not parse info str %s for train %s', train['station_train_code'], train['train_no'])
				continue

			train = Train(
				name=name,
				telecode=telecode
			)
			if train.duplicated:
				yield train
			else:
				parameters = {
					'train_no': telecode,
					'from_station_telecode': 'ABC',
					'to_station_telecode': 'CBA',
					'depart_date': self.date,
				}
				url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?' + urllib.parse.urlencode(parameters)
				request = scrapy.Request(url, callback=self.parseTrainSchedule)
				request.meta['train'] = train
				yield request

	def parse(self, response):
		content = self.pre_parse(response)
		if isinstance(content, str):
			raise CloseSpider(content)

		# Create Records for each day
		parser = self.parseRecords if self.createRecords else self.parseSchedules
		for i in parser(content):
			yield i

	def parseTrainSchedule(self, response):
		def dictForStop(stop):
			departureTime = re.match(r'(\d{2}):(\d{2})', stop['start_time'])
			departureTime = departureTime.groups() if departureTime else None
			arrivalTime = re.match(r'(\d{2}):(\d{2})', stop['arrive_time'])
			arrivalTime = arrivalTime.groups() if arrivalTime else None
			return {
				'station': stop['station_name'],
				'departureTime': timedelta(hours=int(departureTime[0]), minutes=int(departureTime[1]))
				if departureTime else None,
				'arrivalTime': timedelta(hours=int(arrivalTime[0]), minutes=int(arrivalTime[1]))
				if arrivalTime else None,
			}
		jsonData = json.loads(response.body.decode('utf-8'))
		stops = [dictForStop(stop) for stop in jsonData['data']['data']]

		stops[0]['arrivalTime'] = None
		stops[-1]['departureTime'] = None
		train = response.meta['train']
		train['stops'] = stops
		yield train
