from celery import task


@task
def crawl(name):
	from .crawler import crawl_async
	crawl_async(name)
