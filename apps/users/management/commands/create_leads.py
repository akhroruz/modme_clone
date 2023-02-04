from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from users.models import LeadIncrement

faker = Faker()


class Command(BaseCommand):
    help = 'Create some leads'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        c = options.get('total')
        lid_increment = LeadIncrement.objects.all()

        baker.make(
            'users.Lead',
            full_name=cycle(str(faker.first_name() + ' ' + faker.last_name()) for _ in range(c)),
            comment=cycle(faker.text() for _ in range(c)),
            phone=cycle(faker.random_number(digits=8) for _ in range(c)),
            lid_increment=cycle(faker.random_element(lid_increment) for _ in range(c)),

            make_m2m=False,
            _quantity=c
        )
