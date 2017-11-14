from django.contrib import admin
from api import models


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
	list_display = ('name', 'telecode')


@admin.register(models.Train)
class TrainAdmin(admin.ModelAdmin):
	list_display = ('name', 'telecode')


@admin.register(models.Record)
class RecordAdmin(admin.ModelAdmin):
	def name(self, obj):
		return obj.train.name

	list_display = ('name', 'departureDate')
	date_hierarchy = 'departureDate'
