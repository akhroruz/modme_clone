import random
from itertools import cycle

from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Company, Branch, Room, Course

fake = Faker()


class Command(BaseCommand):
    help = '''
        You can create dummy data. Like this:
    * Company      -> 2
    * Branch    -> 5
    '''

    def add_arguments(self, parser):
        parser.add_argument('-c', '--company', type=int, help='Define a company number prefix', )
        parser.add_argument('-b', '--branch', type=int, help='Define a branch number prefix', )
        parser.add_argument('-course', '--course', type=int, help='Define a course number prefix', )
        parser.add_argument('-r', '--room', type=int, help='Define a room number prefix', )
        parser.add_argument('-hd', '--holiday', type=int, help='Define a holiday number prefix', )
        parser.add_argument('-cg', '--coursegroup', type=int, help='Define a coursegroup number prefix', )

    def handle(self, *args, **options):
        # companies
        c = options.get('company', 15)
        baker.make(
            'groups.Company',
            name=cycle(fake.company() for _ in range(c)),
            _quantity=c
        )
        print(c, 'companies is being addded')

        # branches
        b = options.get('branch', 15)
        company_code = ('90', '99', '98', '93', '94')
        company = Company.objects.all()
        baker.make(
            'groups.Branch',
            name=cycle(fake.first_name() for _ in range(c)),
            address=cycle(fake.sentences(nb=100)),
            phone=cycle(random.choice(company_code) + str(fake.random_number(digits=7)).zfill(7) for _ in range(b)),
            about=cycle(fake.sentences(nb=310050)),
            company=cycle(company),
            image='media/img.png',
            _quantity=b
        )
        print(c, 'branches is being addded')

        # course
        course = options.get('course', 15)
        baker.make(
            'groups.Course',
            name=cycle(fake.first_name() for _ in range(course)),
            price=cycle(fake.pyint() * 100 for _ in range(course)),
            description=cycle(fake.sentences(nb=310050)),
            lesson_duration=cycle(fake.pyint() for _ in range(course)),
            course_duration=cycle(fake.pyint() for _ in range(course)),
            image='media/img.png',
            _quantity=b
        )
        print(course, 'courses is being addded')

        # room
        r = options.get('room', 15)
        baker.make(
            'groups.CourseGroup',
            name=cycle(fake.first_name() for _ in range(r)),
            branch=cycle(Branch.objects.all()),
            _quantity=r
        )
        print(r, 'rooms is being addded')

        # holiday
        h = options.get('holiday', 15)
        baker.make(
            'groups.Holiday',
            name=cycle(fake.first_name() for _ in range(h)),
            holiday_date=cycle(fake.date() for _ in range(h)),
            affect_payment=fake.pybool(),
            branch=cycle(Branch.objects.all()),
            _quantity=r
        )
        print(r, 'holidays is being addded')
