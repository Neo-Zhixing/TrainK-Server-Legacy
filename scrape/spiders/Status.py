# -*- coding: utf-8 -*-
import scrapy
import re
import enum
import datetime
from django.utils import timezone
from django.utils.dateparse import parse_duration
from urllib import parse
from train import models


class StatusSpider(scrapy.Spider):
	name = 'Status'
	allowed_domains = ['12306.cn']

	custom_settings = {
		'ITEM_PIPELINES': {
		}
	}

	class TrainStatus(enum.Enum):
		MatchError = enum.auto()      # 无法解析返回的字符串
		ParamError = enum.auto()      # 列车时刻表中无列车的信息，列车不经过站点，或没有该列车
		TimeNotInRange = enum.auto()  # 目前暂无列车到达始发的时间，请稍候重新查询。 不在查询的时间范围（开车前-1 -- +3 h）内。
		NotImplemented = enum.auto()  # 目前D35站尚未开通列车正晚点信息查询服务，请见谅
		Terminal = enum.auto()        # 站点为列车的终点始发站
		Anticipated = enum.auto()     # 预计列车，到达出发时间为
		Actual = enum.auto()          # 列车到达出发时间为

	def parseStr(self, string):
		if re.match(r'^列车时刻表中无[\w/]+次列车的信息$', string):
			return (self.TrainStatus.ParamError, None)
		if re.match(r'^目前[\S]+站尚未开通列车正晚点信息查询服务，请见谅$', string):
			return (self.TrainStatus.NotImplemented, None)
		if re.match(r'^目前暂无[\w/]+次列车[\S]+[到达始发]+时间，请稍候重新查询$', string):
			return (self.TrainStatus.TimeNotInRange, None)
		if re.match(r'^[\S]+为[\w/]+次列车的[终点始发]+站，没有该列车[到达出发]+信息$', string):
			return (self.TrainStatus.Terminal, None)

		match = re.match(r'^预计[\w/]+次列车，[\S]+[到达出发]+时间为(\d+):(\d+)$', string)
		if match:
			return (self.TrainStatus.Anticipated, datetime.timedelta(hours=int(match.group(1)), minutes=int(match.group(2))))

		match = re.match(r'^[\w/]+次列车，((到达\S+的)|(\S+出发))时间为(\d+):(\d+)$', string)
		if match:
			return (self.TrainStatus.Actual, datetime.timedelta(hours=int(match.group(4)), minutes=int(match.group(5))))

		return (self.TrainStatus.MatchError, None)

	def start_requests(self):
		def requestLink(stop, action):
			# Example: http://dynamic.12306.cn/mapping/kfxt/zwdcx/LCZWD/cx.jsp?cz=%BA%CF%B7%CA&cc=T64&cxlx=0&rq=2017-11-17&czEn=-E5-90-88-E8-82-A5&tp=1510912375233
			parameters = {
				'cz': parse.quote(stop.station.name.encode('gbk')),                           # GBK Encoded Station Name
				'cc': stop.train.names[0],                                                    # Train Code
				'cxlx': action.value,                                                         # Action, StatusSpider.TrainAction
				'rq': datetime.date.today().isoformat(),                                      # ISO Formatted current date (Not the date of departure)
				'czEn': parse.quote(stop.station.name.encode('utf-8')).replace('%', '-'),     # UTF-8 Encoded Station Name, replacing % with -
				'tp': int(datetime.datetime.now().timestamp())                                # Current timestamp
			}
			return 'http://dynamic.12306.cn/mapping/kfxt/zwdcx/LCZWD/cx.jsp?' + parse.urlencode(parameters)

		for (action, stops) in (
			(models.TrainAction.Departure, models.Stop.objects.filter(
				departureTimeAnticipated=True,
				departureTime__lte=timezone.now(),
				departureTime__gte=timezone.now() - datetime.timedelta(hours=1))),
			(models.TrainAction.Arrival, models.Stop.objects.filter(
				arrivalTimeAnticipated=True,
				arrivalTime__lte=timezone.now(),
				arrivalTime__gte=timezone.now() - datetime.timedelta(hours=1))),
		):
			for stop in stops:
				request = scrapy.Request(requestLink(stop, action), callback=self.parse)
				request.meta['stop'] = stop
				request.meta['action'] = action
				request.meta['dont_redirect'] = True
				yield request

	def parse(self, response):
		string = response.body.decode('gbk')
		string = re.match(r'^\s+(\S+)\s+$', string)
		if not string:
			self.logger.warning("scrape %s error, result is empty, can't extract prompt string")
			return
		string = string.group(1)
		(status, result) = self.parseStr(string)

		stop = response.meta['stop']
		action = response.meta['action']

		# Result corrections - support for cross-day delays.
		if result:
			scheduledTime = stop.scheduledStop['departureTime'] if action is models.TrainAction.Departure else stop.scheduledStop['arrivalTime']
			scheduledTime = parse_duration(scheduledTime)
			result += datetime.timedelta(days=scheduledTime.days)
			diff = scheduledTime - result
			if diff > datetime.timedelta(hours=4):
				result += datetime.timedelta(days=1)
			elif diff < -datetime.timedelta(hours=4):
				result -= datetime.timedelta(days=1)

		if status is self.TrainStatus.Actual:
			stop.update(action, result, False)
		elif status is self.TrainStatus.Anticipated:
			stop.update(action, result, True)
		elif status is self.TrainStatus.TimeNotInRange or status is self.TrainStatus.NotImplemented:
			stop.update(action=action, anticipated=None)
		else:
			self.logger.info(string)
