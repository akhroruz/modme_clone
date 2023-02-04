from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Branch, Company

fake = Faker()


class Command(BaseCommand):
    help = '''
        You can create dummy data. Like this:
    * Blogs      -> 1000
    * Categories    -> 15
    '''

    def add_arguments(self, parser):
        parser.add_argument('-c', '--company', type=int, help='Define a blog number prefix', )
        parser.add_argument('-b', '--branch', type=int, help='Define a category number prefix', )

    def handle(self, *args, **options):
        b = options.get('company', 1000)

        # Create  dummy data Company
        if c := options.get('branch', 15):
            for _ in range(c):
                Company.objects.create(name=fake.text(50))
            print(c, ' Company is being added')

        # Create dummy data Branch
        company = Company.objects.all()
        print(b, 'Branch is being added')
        baker.make(
            'groups.Branch',
            name=cycle(fake.sentences(nb=100)),
            address=cycle(fake.address()),
            company=cycle(company),
            phone=cycle(fake.phone_number()),
            about=cycle(fake.text()),
            image='media/Без_названия.jpeg',
            _quantity=b
        )
