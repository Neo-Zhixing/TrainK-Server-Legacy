from scrapy.crawler import Crawler
from scrapy import signals
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from billiard import Process

from .spiders.Stations import Spider


class CrawlerScript(Process):
	def __init__(self, spider):
		super(CrawlerScript, self).__init__()
		settings = get_project_settings()
		self.crawler = Crawler(spider.__class__, settings)
		self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		self.spider = spider

	def run(self):
		self.crawler.crawl('stations')
		reactor.run()


def crawl_async():
	spider = Spider()
	crawler = CrawlerScript(spider)
	crawler.start()
	crawler.join()
