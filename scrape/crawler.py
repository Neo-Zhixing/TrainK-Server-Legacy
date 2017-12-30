from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from billiard import Process

from .spiders import Stations, Status, Trains


class CrawlerScript(Process):
	spiders = {
		'stations': Stations.Spider,
		'trains': Trains.Spider,
		'status': Status.Spider
	}

	def __init__(self, name):
		super(CrawlerScript, self).__init__()
		self.spider = self.spiders[name]
		self.crawler = Crawler(self.spider, get_project_settings())
		self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		self.spider = name

	def run(self):
		self.crawler.crawl()
		reactor.run()


def crawl_async(name):
	crawler = CrawlerScript(name)
	crawler.start()
	crawler.join()
