from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Remove all data from the database'

    def handle(self, *args, **options):
        for model in apps.get_models():
            table_name = model._meta.db_table
            cursor = connection.cursor()
            sql = "DROP TABLE %s cascade;" % (table_name,)
            cursor.execute(sql)
