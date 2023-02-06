from itertools import cycle

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Branch
from users.models import User, LeadIncrement
import environ

env = environ.Env(
    DEBUG=(bool, False)
)

faker = Faker()


class Command(BaseCommand):
    help = 'Create some posts'

    def handle(self, *args, **options):
        teacher_role = Group.objects.filter(name='teacher')
        student_role = Group.objects.filter(name='student')
        admin_role = Group.objects.filter(name='admin')
        ceo_role = Group.objects.filter(name='ceo')

        # creating branches
        baker.make(
            'groups.Branch',
            name=cycle(faker.company() for _ in range(3)),
            address=cycle(faker.address() for _ in range(3)),
            phone=cycle(faker.random_number() for _ in range(3)),
            about=cycle(faker.text(max_nb_chars=250) for _ in range(3)),
            image='media/img.png',
            _quantity=3,
        )
        branch = Branch.objects.all()

        # creating teachers
        baker.make(
            'users.User',
            first_name=cycle(faker.first_name() for _ in range(20)),
            last_name=cycle(faker.last_name() for _ in range(20)),
            birth_date=cycle(faker.date_of_birth(maximum_age=70, minimum_age=7) for _ in range(20)),
            phone=cycle(faker.random_number(digits=9) for _ in range(20)),
            gender=cycle(faker.random_element(User.GenderChoose) for _ in range(20)),
            role=teacher_role,
            branch=cycle(faker.random_element(branch) for _ in range(20)),
            comment=cycle(faker.text() for _ in range(20)),
            password=make_password(env('USER_PR')),
            make_m2m=False,
            _quantity=20
        )

        # creating students
        baker.make(
            'users.User',
            first_name=cycle(faker.first_name() for _ in range(100)),
            last_name=cycle(faker.last_name() for _ in range(100)),
            birth_date=cycle(faker.date_of_birth(maximum_age=70, minimum_age=7) for _ in range(100)),
            phone=cycle(faker.random_number(digits=9) for _ in range(100)),
            gender=cycle(faker.random_element(User.GenderChoose) for _ in range(100)),
            role=student_role,
            branch=cycle(faker.random_element(branch) for _ in range(100)),
            comment=cycle(faker.text() for _ in range(100)),
            password=make_password(env('USER_PR')),

            make_m2m=False,
            _quantity=100
        )

        # creating admins
        baker.make(
            'users.User',
            first_name=cycle(faker.first_name() for _ in range(7)),
            last_name=cycle(faker.last_name() for _ in range(7)),
            birth_date=cycle(faker.date_of_birth(maximum_age=70, minimum_age=7) for _ in range(7)),
            phone=cycle(faker.random_number(digits=9) for _ in range(7)),
            gender=cycle(faker.random_element(User.GenderChoose) for _ in range(7)),
            role=admin_role,
            branch=cycle(faker.random_element(branch) for _ in range(7)),
            comment=cycle(faker.text() for _ in range(7)),
            password=make_password(env('USER_PR')),

            make_m2m=False,
            _quantity=7
        )

        # creating ceo
        baker.make(
            'users.User',
            first_name=cycle(faker.first_name() for _ in range(2)),
            last_name=cycle(faker.last_name() for _ in range(2)),
            birth_date=cycle(faker.date_of_birth(maximum_age=70, minimum_age=7) for _ in range(2)),
            phone=cycle(faker.random_number(digits=9) for _ in range(2)),
            gender=cycle(faker.random_element(User.GenderChoose) for _ in range(2)),
            role=ceo_role,
            branch=cycle(faker.random_element(branch) for _ in range(2)),
            comment=cycle(faker.text() for _ in range(2)),
            password=make_password(env('USER_PR')),

            make_m2m=False,
            _quantity=2
        )

        # creating lead_increments
        baker.make(
            'users.LeadIncrement',
            name=cycle(faker.sentence() for _ in range(5)),

            _quantity=5
        )
        lead_increment = LeadIncrement.objects.all()

        # creating leads
        baker.make(
            'users.Lead',
            full_name=cycle(str(faker.first_name() + ' ' + faker.last_name()) for _ in range(10)),
            comment=cycle(faker.text() for _ in range(10)),
            phone=cycle(faker.random_number(digits=8) for _ in range(10)),
            lead_increment=cycle(faker.random_element(lead_increment) for _ in range(10)),

            make_m2m=False,
            _quantity=10
        )

        user = User.objects.all()

        baker.make(
            'users.Comment',
            text=cycle(faker.text() for _ in range(20)),
            user=cycle(faker.random_element(user) for _ in range(20)),

            _quantity=20
        )
