from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from users.models import User

faker = Faker()


class Command(BaseCommand):
    help = 'Create some lead increments'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        c = options.get('total')

        baker.make(
            'users.LeadIncrement',
            name=cycle(faker.sentence() for _ in range(c)),

            _quantity=c
        )
