# -*- coding: utf-8 -*-
import scrapy
import json
import urllib
from scrapy.exceptions import CloseSpider
from scrape.items import Train, Stop


class TrainsSpider(scrapy.Spider):
	name = 'Trains'
	allowed_domains = ['12306.cn']
	start_urls = ['https://kyfw.12306.cn/otn/resources/js/query/train_list.js']
	custom_settings = {
		'ITEM_PIPELINES': {
			'scrape.pipelines.TrainSavingPipeline': 400
		}
	}

	def parse(self, response):
		if not hasattr(self, 'date'):
			raise CloseSpider('Cannot get argument date')
		data = response.body.decode('utf-8')
		data = data[data.index('=') + 1:]  # REMOVE var train_list =
		jsonData = json.loads(data)
		if not jsonData:
			raise CloseSpider('Can not parse data as JSON')
		jsonData = jsonData.get(self.date)
		if not jsonData:
			raise CloseSpider('Can not find designated date')

		for prefix in jsonData.keys():
			for train in jsonData[prefix]:
				import re
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
				if train.originalTrain:
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
		jsonData = json.loads(response.body.decode('utf-8'))
		stops = []
		for stop in jsonData['data']['data']:
			stops.append(Stop(
				station=stop['station_name'],
				departureTime=stop['start_time'],
				arrivalTime=stop['arrive_time']
			))
		stops[0]['arrivalTime'] = None
		stops[-1]['departureTime'] = None
		train = response.meta['train']
		train['stops'] = stops
		yield train
