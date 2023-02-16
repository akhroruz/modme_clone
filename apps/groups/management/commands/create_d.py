from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Company, Branch, Course

faker = Faker()


class Command(BaseCommand):
    help = 'Create some posts'
    # creating company
    baker.make(
        'groups.Company',
        name=cycle(faker.company() for _ in range(3)),
    )
    company = Company.objects.all()

    # creating branches
    baker.make(
        'groups.Branch',
        name=cycle(faker.company() for _ in range(7)),
        address=cycle(faker.address() for _ in range(7)),
        phone=cycle(faker.random_number() for _ in range(7)),
        about=cycle(faker.text(max_nb_chars=255) for _ in range(7)),
        image='media/img.png',
        _quantity=3,
    )
    branch = Branch.objects.all()

    #  creating room
    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='total count of creating posts')

    def handle(self, *args, **options):
        total = options.get('total')
        branch = Branch.objects.all()
        course = Course.objects.all()

        baker.make(
            'groups.Branch',
            name=cycle(faker.building_number() for _ in total),
            branch=cycle(faker.random_element(branch) for _ in total),

            _quantity=total
        )

        # creating course
        baker.make(
            'groups.Course',
            name=cycle(faker.name()),
            price=faker.random_number(digits=6),
            description=cycle(faker.text()),
            image=cycle(faker.image()),
            lesson_duration=2,
            course_duration=9,
            branch=cycle(faker.random_choices(course)),
        )
        

