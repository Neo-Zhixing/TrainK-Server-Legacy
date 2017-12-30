# -*- coding: utf-8 -*-
import scrapy
from ..items import Station


class Spider(scrapy.Spider):
	name = 'Stations'
	allowed_domains = ['12306.cn']
	start_urls = ['https://kyfw.12306.cn/otn/resources/js/framework/station_name.js']

	def parse(self, response):
		data = response.body.decode('utf-8')
		data = data[data.index('@') + 1:data.index(';') - 1]
		data += '@'

		for i in range(0, data.count("@")):
			# abbreviation1 = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # wln some unknown telecode.

			name = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # 乌鲁木齐南

			telecode = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # WMR

			spell = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # wulumuqinan

			abbreviation = data[:data.index('|')]
			data = data[data.index("|") + 1:]  # wlmqn

			# number = data[:data.index('@')]
			data = data[data.index('@') + 1:]

			yield Station(name=name, telecode=telecode, spell=spell, abbreviation=abbreviation)
