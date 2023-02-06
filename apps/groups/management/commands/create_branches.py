from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

fake = Faker()


class Command(BaseCommand):
    help = '''
        You can create dummy data. Like this:
    * Company      -> 2
    * Branch    -> 5
    '''

    def add_arguments(self, parser):
        parser.add_argument('-c', '--company', type=int, help='Define a company number prefix', )
        # parser.add_argument('-b', '--branch', type=int, help='Define a branch number prefix', )

    def handle(self, *args, **options):
        # Create  dummy data Category
        if c := options.get('company', 15):
            baker.make(
                'groups.Company',
                name=cycle(fake.company() for _ in range(c)),
                _quantity=c
            )

        #     for _ in range(c):
        #         Category.objects.create(name=fake.text(50))
        #     print(c, 'categories is being addded')
        #
        # # Create dummy data Product
        # b = options.get('blog', 1000)
        # categories = Category.objects.all()
        # regions = Region.objects.all()
        # print(b, 'blogs is being addded')
        # baker.make(
        #     'apps.Branch',
        #     title=cycle(fake.sentences(nb=100)),
        #     text=cycle(fake.sentences(nb=310050)),
        #     _quantity=b,
        #     make_m2m=True
        # )
