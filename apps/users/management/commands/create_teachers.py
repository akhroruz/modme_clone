from itertools import cycle

from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Branch
from users.models import User

faker = Faker()


class Command(BaseCommand):
    help = 'Create some posts'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        total = options.get('total')
        role = Group.objects.filter(name='teacher')
        branch = Branch.objects.all()
        baker.make(
            'users.User',
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            birth_date=faker.date_of_birth(),
            phone=faker.random_number(digits=9),
            gender=faker.random_element(User.GenderChoose),
            role=role,
            branch=cycle(faker.random_choices(branch)),
            make_m2m=False,
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
