from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

# from groups.models import Branch


class Command(BaseCommand):
    help = 'Create some posts'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        total = options.get('total')
        faker = Faker()
        for i in range(total):
            baker.make('groups.Room',
                       name=faker.building_number(), make_m2m=False,
                       # branch=faker.choise_element(Branch)
                       )
