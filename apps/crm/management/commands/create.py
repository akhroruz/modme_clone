import random
from itertools import cycle

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from faker import Faker
from model_bakery import baker

from groups.models import Company, Branch, Course, Room
from users.models import User, LeadIncrement, Archive

fake = Faker()


class Command(BaseCommand):
    help = '''
        You can create dummy data. Like this:
    * Company           -> 2
    * Branch            -> 15
    * Course            -> 15
    * Room              -> 15
    * Holiday           -> 15
    * Course group      -> 15
    * User              -> 15
    * Archive           -> 15
    * Lead              -> 15
    * Lead increment    -> 15
    '''

    def add_arguments(self, parser):
        parser.add_argument('-c', '--company', type=int, help='Define a company number prefix', )
        parser.add_argument('-b', '--branch', type=int, help='Define a branch number prefix', )
        parser.add_argument('-course', '--course', type=int, help='Define a course number prefix', )
        parser.add_argument('-r', '--room', type=int, help='Define a room number prefix', )
        parser.add_argument('-hd', '--holiday', type=int, help='Define a holiday number prefix', )
        parser.add_argument('-gr', '--coursegroup', type=int, help='Define a group number prefix', )
        parser.add_argument('-u', '--user', type=int, help='Define a user number prefix', )
        parser.add_argument('-a', '--archive', type=int, help='Define a archive number prefix', )
        parser.add_argument('-li', '--lead_increment', type=int, help='Define a lead increment number prefix', )
        parser.add_argument('-l', '--lead', type=int, help='Define a lead number prefix', )

    def handle(self, *args, **options):
        company_code = ('90', '99', '98', '93', '94')
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
            branch=cycle(Branch.objects.all()),
            name=cycle(fake.first_name() for _ in range(course)),
            price=cycle(fake.pyint() * 100 for _ in range(course)),
            description=cycle(fake.sentences(nb=310050)),
            lesson_duration=cycle(fake.pyint() for _ in range(course)),
            course_duration=cycle(fake.pyint() for _ in range(course)),
            image='media/img.png',
            make_m2m=True,
            _quantity=b
        )
        print(course, 'courses is being addded')

        # room
        r = options.get('room', 15)
        baker.make(
            'groups.Room',
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

        # archive
        a = options.get('archive', 15)
        baker.make(
            'users.Archive',
            name=cycle(fake.first_name() for _ in range(a)),
            _quantity=a
        )
        print(a, 'archives is being addded')

        # user
        u = options.get('user', 15)
        baker.make(
            'users.User',
            first_name=cycle(fake.first_name() for _ in range(u)),
            last_name=cycle(fake.last_name() for _ in range(u)),
            birth_date=cycle(fake.date() for _ in range(u)),
            phone=cycle(random.choice(company_code) + str(fake.random_number(digits=7)).zfill(7) for _ in range(u)),
            gender=cycle(fake.random_element(User.GenderChoose) for _ in range(100)),
            role=cycle(Group.objects.all()),
            branch=cycle(Branch.objects.all()),
            archive=cycle(Archive.objects.all()),
            comment=cycle(fake.text() for _ in range(u)),
            password=make_password('1'),
            photo='media/img.png',
            is_archive=False,
            make_m2m=True,
            _quantity=u
        )

        print(c, 'users is being addded')

        # lead increment
        li = options.get('lead_increment', 15)
        baker.make(
            'users.LeadIncrement',
            name=cycle(fake.first_name() for _ in range(li)),
            _quantity=li
        )

        print(li, 'lead increments is being addded')

        # lead
        l = options.get('lead', 15)
        baker.make(
            'users.Lead',
            full_name=cycle(fake.first_name() for _ in range(l)),
            comment=cycle(fake.text() for _ in range(l)),
            phone=cycle(random.choice(company_code) + str(fake.random_number(digits=7)).zfill(7) for _ in range(u)),
            lid_increment=cycle(LeadIncrement.objects.all()),
            _quantity=l
        )
        print(l, 'lead is being addded')

        # course group
        gr = options.get('coursegroup', 15)
        baker.make(
            'groups.CourseGroup',
            name=cycle(fake.first_name() for _ in range(gr)),
            status=cycle(fake.random_element(User.GenderChoose) for _ in range(100)),
            start_date=cycle(fake.date() for _ in range(gr)),
            end_date=cycle(fake.date() for _ in range(gr)),
            branch=cycle(Branch.objects.all()),
            teachers=cycle(User.objects.all()),
            students=cycle(User.objects.all()),
            course=cycle(Course.objects.all()),
            room=cycle(Room.objects.all()),
            make_m2m=True,
            _quantity=gr
        )
        print(gr, 'groups is being addded')
