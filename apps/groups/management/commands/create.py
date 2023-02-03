import random
from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Branch

fake = Faker()


class Command(BaseCommand):
    help = '''
        You can create dummy data. Like this:
    * Branches   -> 10
    '''

    def add_arguments(self, parser):
        parser.add_argument('-b', '--branch', type=int, help='Define a branch number prefix', )

    def handle(self, *args, **options):
        b = options.get('branch', 10)

        # Create  dummy data Category
        # if c := options.get('category', 15):
        #     for _ in range(c):
        #         Category.objects.create(name=fake.text(50))
        #     print(c, 'categories is being addded')

        # Create dummy data Product
        # categories = Category.objects.all()
        print(b, 'Branches is being addded')
        baker.make(
            'groups.Branch',
            name=cycle(fake.sentences(nb=1)),
            address=cycle(fake.sentences(nb=100)),
            phone=cycle(fake.ean(length=8, prefixes=('94', '93'))),
            about=cycle(fake.sentences(nb=310050)),
            image='media/img.png',
            _quantity=b,
            # make_m2m=True
        )
