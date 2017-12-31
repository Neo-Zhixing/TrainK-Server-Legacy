from celery import task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from billiard import Process


@task
def crawl(*args, **kwargs):
	crawler = CrawlerProcess(get_project_settings())
	crawler.crawl(*args, **kwargs)
	process = Process(target=crawler.start)
	process.start()
	process.join()
	crawler.stop()
