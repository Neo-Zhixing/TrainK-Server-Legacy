from scrapy.exceptions import DropItem


class DjangoDatabaseSavePipeline(object):
	def process_item(self, item, spider):
		if hasattr(item, 'duplicated'):
			if item.duplicated:
				msg = ''
				if hasattr(item, 'duplicatedWillDiscard'):
					msg = item.duplicatedWillDiscard()
				raise DropItem("Duplicate item found. %s" % msg)

		if hasattr(item, 'itemWillCreate'):
			msg = item.itemWillCreate()
			if msg:
				raise DropItem("Saving error, %s" % msg)
		item.save()
		return item
