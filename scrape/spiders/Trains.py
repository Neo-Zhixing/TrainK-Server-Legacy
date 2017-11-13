import scrapy
import json
import urllib
from datetime import timedelta
from scrapy.exceptions import CloseSpider
from scrapy.exceptions import DropItem
import re
import logging
from scrape.items import Train, Record
from api import models


class Spider(scrapy.Spider):
	name = 'Trains'
	allowed_domains = ['12306.cn']
	start_urls = ['https://kyfw.12306.cn/otn/resources/js/query/train_list.js']
	createRecords = False
	date = None
	keys = None

	def parse(self, response):
		# Check the existence of required parameter Date
		if not self.date:
			raise CloseSpider('Cannot get argument "date"')

		# Parse page info into JSON
		data = response.body.decode('utf-8')
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
		content = []
		for prefix in keys:
			contentInPrefix = jsonData.get(prefix)
			if contentInPrefix:
				content.extend(contentInPrefix)
			else:
				self.logger.warning('Train prefix %s not exist', prefix)
				continue

		# Create Records for each day
		if self.createRecords:
			for train in content:
				record = Record(
					departureDate=self.date,
					train=train['train_no'],
				)
				yield record
			return

		# Parse Train Schedules
		else:
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


class Pipeline(object):
	def process_item(self, item, spider):
		if isinstance(item, Record):
			if models.Record.objects.filter(departureDate=item['departureDate'], train__telecode=item['train']).exists():
				raise DropItem('Record exist for %s at %s', item['train'], item['departureDate'])
			train = models.Train.objects.filter(telecode=item['train'])
			if not train.exists():
				raise DropItem('Train %s schedule not exist!', item['train'])
			if train.count() > 1:
				raise DropItem('Duplicated trains exist for %s', item['train'])
			train = train.first()
			item['train'] = train
			models.Record(departureDate=item['departureDate'], train=train).save()

			return item

		originalTrain = item.originalTrain
		if originalTrain:
			if item['name'] in originalTrain.names:
				raise DropItem('Duplicated Item %s, telecode %s', item['name'], item['telecode'])
			else:
				originalTrain.names.append(item['name'])
				originalTrain.save()
				logging.info('Merged with %s, telecode %s', originalTrain.name, originalTrain.telecode)
				return item
		else:
			train = models.Train(names=[item['name']], telecode=item['telecode'])
			train.save()
			for stop in item['stops']:
				station = models.Station.objects.filter(name=stop['station'])
				if station.exists():
					station = station.first()
				else:
					station = models.Station(name=stop['station'])
					station.save()
					logging.info('Station %s not exist. Created.', station.name)
				newStop = models.Stop(station=station, departureTime=stop['departureTime'], arrivalTime=stop['arrivalTime'])
				newStop.save()
				train.stops.add(newStop)
			train.save()
			return item
