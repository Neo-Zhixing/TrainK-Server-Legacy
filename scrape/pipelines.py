from scrapy.exceptions import DropItem
import logging
from api import models


class DjangoDatabaseSavePipeline(object):
	def process_item(self, item, spider):
		if hasattr(item, 'duplicated'):
			if item.duplicated:
				raise DropItem("Duplicate item found.")
		item.save()
		return item


