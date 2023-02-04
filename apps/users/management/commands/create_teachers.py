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
            first_name=cycle(faker.first_name() for _ in range(total)),
            last_name=cycle(faker.last_name() for _ in range(total)),
            birth_date=cycle(faker.date_of_birth(maximum_age=70, minimum_age=7) for _ in range(total)),
            phone=cycle(faker.random_number(digits=9) for _ in range(total)),
            gender=cycle(faker.random_element(User.GenderChoose) for _ in range(total)),
            role=role,
            branch=cycle(faker.random_element(branch) for _ in range(total)),
            comment=cycle(faker.text() for _ in range(total)),
            make_m2m=False,
            _quantity=total
        )
