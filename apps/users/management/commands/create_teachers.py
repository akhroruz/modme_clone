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
        role = Role.objects.filter(name='Teacher')
        for i in range(total):
            full_name = faker.name()
            baker.make('users.User', make_m2m=True,
                       full_name=full_name,
                       first_name=full_name.split()[0],
                       last_name=full_name.split()[-1],
                       birth=faker.date_of_birth(),
                       phone="9" + str(faker.random_number(digits=8, fix_len=False)),
                       gender=faker.random_element(User.GenderChoose),
                       role=role
                       )

            # User.objects.get_or_create(
            #     role=faker.random_choices(Role.objects.all()),
            #     branch=faker,
            #     balance=faker,
            #     created_at=faker.date_time_between_dates(),
            #     # status=User.StatusChoise.ACTIVE,
            #
            # )
