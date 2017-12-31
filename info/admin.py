from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from . import models
from scrape.tasks import crawl


class ScrapableMixin():
	change_list_template = 'admin/scrapable_list.html'

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [
			path('scrape/', self.admin_site.admin_view(self.scrape_view), name='info_scrape_' + self.model._meta.label)
		]
		return my_urls + urls

	def scrape_view(self, request):
		self.crawl()
		context = dict(self.admin_site.each_context(request))
		context.update({
			'opts': self.model._meta,
			'title': 'Scraping %s' % self.model._meta.verbose_name_plural
		})
		return render(request, 'admin/scrape.html', context)

	def crawl(self):
		crawl.delay(self.model._meta.verbose_name_plural.title())


@admin.register(models.Station)
class StationAdmin(ScrapableMixin, admin.ModelAdmin):
	list_display = ('id', 'name', 'telecode', 'abbreviation', 'spell')
	search_fields = ('id', 'name', 'telecode', 'abbreviation', 'spell')


@admin.register(models.Train)
class TrainAdmin(ScrapableMixin, admin.ModelAdmin):
	list_display = ('name', 'telecode')
	search_fields = ('names', 'telecode')


@admin.register(models.Record)
class RecordAdmin(ScrapableMixin, admin.ModelAdmin):

	def name(self, obj):
		return obj.train.name

	list_display = ('name', 'departureDate')
	search_fields = ('name', 'train__telecode')
	date_hierarchy = 'departureDate'
