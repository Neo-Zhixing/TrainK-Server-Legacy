from scrapy.exceptions import DropItem


class DjangoDatabaseSavePipeline(object):
	def process_item(self, item, spider):
		if hasattr(item, 'duplicated'):
			if item.duplicated:
				msg = item.duplicatedWillDiscard()
				raise DropItem("Duplicate item found. %s" % msg)

		if hasattr(item, 'itemWillCreate'):
			item.itemWillCreate()
		item.save()
		return item
