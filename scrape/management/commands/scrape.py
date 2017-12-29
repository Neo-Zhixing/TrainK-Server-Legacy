from django.core.management.base import BaseCommand, CommandError
import os


class Command(BaseCommand):
	help = 'Run celery to perform scraping actions or tasks.'

	def add_arguments(self, parser):
		parser.add_argument('role', nargs='?', type=str, help='worker/beater/watcher')

	def handle(self, *args, **options):
		role = options['role']
		if role == 'worker':
			os.system('celery -A TrainK worker -l info')
		elif role == 'beater':
			os.system('celery -A TrainK beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler')
		elif role == 'watcher':
			os.system('flower -A TrainK --port=5555')
		else:
			raise CommandError('Role "%s" does not exist' % role)
