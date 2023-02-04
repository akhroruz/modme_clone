from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker
from groups.models import Course

faker = Faker()


class Command(BaseCommand):
    help = 'Create some course'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating courses')

    def handle(self, *args, **options):
        total = options.get('total')
        course = Course.objects.all()
        baker.make(
            'users.User',
            name=cycle(faker.name()),
            price=faker.random_number(digits=6),
            description=cycle(faker.text()),
            image=cycle(faker.image()),
            lesson_duration=2,
            course_duration=9,
            branch=cycle(faker.random_choices(course)),
            make_m2m=False,
            _quantity=total
        )
