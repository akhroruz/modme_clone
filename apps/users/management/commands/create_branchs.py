from django.core.management import BaseCommand
from faker import Faker
from faker.utils.text import slugify

from apps.groups.models import Role
from apps.users.models import User
from model_bakery import baker


class Command(BaseCommand):
    help = 'Create some posts'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        total = options.get('total')
        faker = Faker()
        for i in range(total):
            baker.make('groups.Branch',
                       name=faker.company(),
                       address=faker.address(),
                       phone_number="9" + str(faker.random_number(digits=8, fix_len=False)),
                       about=faker.text(max_nb_chars=160),
                       image=faker.image_url(),
                       )
