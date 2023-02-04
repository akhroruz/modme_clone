from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

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
            name=fake.company(),
            address=fake.address(),
            phone=fake.random_number(),
            about=fake.text(max_nb_chars=250),
            image='media/img.png',
            _quantity=b,
            # make_m2m=True
        )
