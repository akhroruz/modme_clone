from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from users.models import User

faker = Faker()


class Command(BaseCommand):
    help = 'Create some comments'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        c = options.get('total')
        user = User.objects.all()

        baker.make(
            'users.Comment',
            text=cycle(faker.text() for _ in range(c)),
            user=cycle(faker.random_element(user) for _ in range(c)),

            _quantity=c
        )
