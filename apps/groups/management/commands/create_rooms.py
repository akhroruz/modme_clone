from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Branch

faker = Faker()


class Command(BaseCommand):
    help = 'Create some branchs'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        total = options.get('total')
        branch = Branch.objects.all()

        baker.make(
            'groups.Branch',
            name=cycle(faker.building_number() for _ in total),
            branch=cycle(faker.random_element(branch) for _ in total),

            _quantity=total
        )
