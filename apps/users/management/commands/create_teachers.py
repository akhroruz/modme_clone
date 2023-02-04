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
        # role = Role.objects.filter(name='Teacher')
        baker.make(
            'users.User',
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            birth=faker.date_of_birth(),
            phone=faker.random_number(digits=9, fix_len=False),
            gender=faker.random_element(User.GenderChoose),
            # role=role,
            make_m2m=True,
            _quantity=total
        )

        # User.objects.get_or_create(
        #     role=faker.random_choices(Role.objects.all()),
        #     branch=faker,
        #     balance=faker,
        #     created_at=faker.date_time_between_dates(),
        #     # status=User.StatusChoise.ACTIVE,
        #
        # )
