from scrapy.exceptions import DropItem
import logging

###
# BULK CREATE:	SET save_batch_size property in spiders to numbers other than 1 to activate.
# Use Only when a spider yield one sort of object.
###


class DjangoDatabaseSavePipeline(object):
	logger = logging.getLogger('scrape.pipelines.DjangoDatabaseSavePipeline')
	itemsToSave = {}

	def bulkCreate(self, keys=None):
		if not keys:
			keys = self.itemsToSave.keys()
		self.logger.info('Creating database records for %s', keys)
		for key in keys:
			key.objects.bulk_create(self.itemsToSave[key])
			self.itemsToSave[key] = []

	def open_spider(self, spider):
		if not hasattr(spider, 'save_batch_size'):
			spider.save_batch_size = 1
		self.bulkCreateDisabled = spider.save_batch_size == 1

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

		bulkCreateDisabled = type(item).save_batch_size == 1
		djangoItem = item.save(commit=bulkCreateDisabled)

		if not bulkCreateDisabled:
			saveTo = self.itemsToSave.get(item.django_model)
			if not saveTo:
				saveTo = []
				self.itemsToSave[item.django_model] = saveTo
			saveTo.append(djangoItem)
			if len(saveTo) > type(item).save_batch_size:
				self.bulkCreate([item.django_model])

		return item

	def close_spider(self, spider):
		self.bulkCreate()
