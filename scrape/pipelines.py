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


class TrainSavingPipeline(object):
	def process_item(self, item, spider):
		originalTrain = item.originalTrain
		if originalTrain:
			if item['name'] in originalTrain.names:
				raise DropItem('Duplicated Item %s, telecode %s', item['name'], item['telecode'])
			else:
				originalTrain.names.append(item['name'])
				originalTrain.save()
				logging.info('Merged with %s, telecode %s', originalTrain.name, originalTrain.telecode)
				return item
		else:
			train = models.Train(names=[item['name']], telecode=item['telecode'])
			train.save()
			for stop in item['stops']:
				station = models.Station.objects.filter(name=stop['station'])
				if station.exists():
					station = station.first()
				else:
					station = models.Station(name=stop['station'])
					station.save()
					logging.info('Station %s not exist. Created.', station.name)
				newStop = models.Stop(station=station, departureTime=stop['departureTime'], arrivalTime=stop['arrivalTime'])
				newStop.save()
				train.stops.add(newStop)
			train.save()
			return item
