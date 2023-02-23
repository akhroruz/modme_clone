from datetime import date, time

import pytest

from groups.models import Company, Branch, Room, Course, Holiday, Group
from users.models import User


@pytest.mark.django_db
class TestCompanyModel:
    def test_create_company(self): # noqa
        data = {'name': 'PDP'}
        company_count = Company.objects.count()
        company = Company.objects.create(**data)
        assert company.name == data['name']
        assert str(company) == company.name
        assert company_count + 1 == Company.objects.count()


@pytest.mark.django_db
class TestBranchModel:
    def test_branch(self):
        company = Company.objects.create(name='Test Company')
        data = {
            'name': 'Test Branch',
            'address': 'Test Address',
            'company': company,
            'phone': '949343943',
            'about': 'Test About',
            'image': 'test_image.png'
        }
        branch_count = Branch.objects.count()
        branch = Branch.objects.create(**data)
        assert branch.name == data['name']
        assert branch.address == data['address']
        assert branch.phone == data['phone']
        assert branch.about == data['about']
        assert branch.image == data['image']
        assert str(branch) == branch.name
        assert str(company) == company.name
        assert branch.company.name == 'Test Company'
        assert branch_count + 1 == Branch.objects.count()


@pytest.mark.django_db
class TestRoomModel:

    def test_room(self):
        company = Company.objects.create(name='PDP')
        branch = Branch.objects.create(
            name='test branch',
            address='test branch address',
            phone='934341245',
            about='test branch about',
            image='branch_image/.png',
            company=company
        )
        room_count = Room.objects.count()
        data = {'name': 'test_room', 'branch': branch}
        room = Room.objects.create(**data)

        assert room.name == data['name']
        assert room.branch == branch
        assert str(room) == room.name
        assert room_count == Room.objects.count() - 1


@pytest.mark.django_db
class TestCourseModel:
    def test_create_course(self):
        company = Company.objects.create(name='test_name')

        data = {
            'name': 'test_name',
            'price': 500,
            'description': 'test_description',
            'image': 'test_image.png',
            'lesson_duration': 3,
            'course_duration': 6,
            'company': company
        }
        course_count = Course.objects.count()
        course = Course.objects.create(**data)
        assert course.name == data['name']
        assert course.price == data['price']
        assert course.description == data['description']
        assert course.image == data['image']
        assert course.lesson_duration == data['lesson_duration']
        assert course.course_duration == data['course_duration']
        assert course.company == company
        assert str(course) == course.name
        assert course_count == Company.objects.count() - 1


@pytest.mark.django_db
class TestHolidayModel:
    def test_holiday(self):
        company = Company.objects.create(name='test_company')  # noqa
        branch = Branch.objects.create(
            name='test branch',
            address='test branch address',
            phone='934341245',
            about='test branch about',
            image='branch_image.png',
            company=company
        )
        data = {
            'name': 'test_name',
            'holiday_date': date(2023, 12, 25),
            'affect_payment': False,
            'branch': branch
        }
        holiday_count = Holiday.objects.count()
        holiday = Holiday.objects.create(**data)

        assert holiday.name == data['name']
        assert holiday.holiday_date == data['holiday_date']
        assert not holiday.affect_payment
        assert branch == branch
        assert str(holiday) == holiday.name
        assert holiday_count + 1 == Holiday.objects.count()


@pytest.mark.django_db
class TestGroupModel:
    def test_group(self):
        company = Company.objects.create(name='test_company')
        branch = Branch.objects.create(
            name='test branch',
            address='test branch address',
            phone='934341245',
            about='test branch about',
            image='branch_image.png',
            company=company
        )
        room = Room.objects.create(name='test_room', branch=branch)
        course = Course.objects.create(
            name='test_name',
            price=1500,
            description='test_description',
            image='test_image.png',
            lesson_duration=2,
            course_duration=6,
            company=company
        )
        user = User.objects.create_user(phone='1233434', password='test_password')

        group_data = {
            'name': 'test_name',
            'days': 'Odd days',
            'status': 'active',
            'room': room,
            'teacher': user,
            'start_time': time(hour=9, minute=00),
            'end_time': time(hour=12, minute=30),
            'course': course,
            'branch': branch,
            'start_date': date(2023, 2, 23),
            'end_date': date(2023, 5, 23),
            'tags': ['test_tag1']
        }
        group_count = Group.objects.count()
        group = Group.objects.create(**group_data)
        group.students.add(user)

        assert group.name == group_data['name']
        assert group.days == group_data['days']
        assert group.status == group_data['status']
        assert group.room == room
        assert group.start_time == group_data['start_time']
        assert group.end_time == group_data['end_time']
        assert group.course == course
        assert group.branch == branch
        assert group.start_date == group_data['start_date']
        assert group.end_date == group_data['end_date']
        assert group.tags == group_data['tags']
        assert group_count + 1 == Group.objects.count()
