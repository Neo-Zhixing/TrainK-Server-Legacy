# -*- coding: utf-8 -*-
import scrapy
from scrape.items import Station


class StationsSpider(scrapy.Spider):
	name = 'Stations'
	allowed_domains = ['12306.cn']
	start_urls = ['https://kyfw.12306.cn/otn/resources/js/framework/station_name.js']

	def parse(self, response):
		data = response.body.decode('utf-8')
		data = data[data.index('@') + 1:data.index(';') - 1]
		data += '@'

		for i in range(0, data.count("@")):
			# abbriviation1 = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # bjb

			name = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # the chinese name

			telecode = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # VAP

			# spell = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # beijingbei

			# abbriviation2 = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # bjb

			# number = data[:data.index('@')]
			data = data[data.index('@') + 1:]

			yield Station(name=name, telecode=telecode)
