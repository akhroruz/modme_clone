from datetime import date, time

import pytest

from groups.models import Company, Branch, Room, Course, Holiday, Group
from users.models import User


@pytest.mark.django_db
class TestCompanyModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='PDP')
        return company

    def test_company(self, company):
        assert company.name == 'PDP'
        assert str(company) == company.name


@pytest.mark.django_db
class TestBranchModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='Test Company')
        return company

    @pytest.fixture
    def branch(self, company):  # noqa
        branch = Branch.objects.create(
            name='Test Branch',
            address='Test Address',
            company=company,
            phone='1234567890',
            about='Test About',
            image='test.png'
        )
        return branch

    def test_branch_model(self, branch, company):  # noqa
        assert branch.name == 'Test Branch'
        assert branch.address == 'Test Address'
        assert branch.phone == '1234567890'
        assert branch.about == 'Test About'
        assert branch.image == 'test.png'
        assert str(branch) == branch.name
        assert str(company) == company.name
        assert branch.company.name == 'Test Company'


@pytest.mark.django_db
class TestRoomModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='ECMA')
        return company

    @pytest.fixture
    def branch(self, company):
        branch = Branch.objects.create(
            name='test_name',
            address='test_address',
            company=company,
            phone='932233445',
            about='test_about',
            image='test_image.png'
        )
        return branch

    @pytest.fixture
    def room(self, branch):
        room = Room.objects.create(
            name='test_name',
            branch=branch
        )
        return room

    def test_room_model(self, room, branch):
        assert room.name == 'test_name'
        assert room.branch == branch
        assert str(room) == room.name


@pytest.mark.django_db
class TestCourseModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='test_name')
        return company

    @pytest.fixture
    def course(self, company):
        course = Course.objects.create(
            name='test_name',
            price=500,
            description='test_description',
            image='test_image.png',
            lesson_duration=3,
            course_duration=6,
            company=company
        )
        return course

    def test_course_model(self, company, course):
        assert course.name == 'test_name'
        assert course.price == 500
        assert course.description == 'test_description'
        assert course.image == 'test_image.png'
        assert course.lesson_duration == 3
        assert course.course_duration == 6
        assert course.company == company
        assert str(course) == course.name


@pytest.mark.django_db
class TestHolidayModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='test_company')
        return company

    @pytest.fixture
    def branch(self, company):
        branch = Branch.objects.create(
            name='test_name',
            address='test_address',
            company=company,
            phone='933432343',
            about='test_about',
            image='test_image.png',
        )
        return branch

    @pytest.fixture
    def holiday(self, branch):
        holiday = Holiday.objects.create(
            name='test_name',
            holiday_date=date(2023, 12, 25),
            affect_payment=False,
            branch=branch
        )
        return holiday

    def test_holiday_model(self, holiday, branch):
        assert holiday.name == 'test_name'
        assert holiday.holiday_date == date(2023, 12, 25)
        assert not holiday.affect_payment
        assert branch == branch
        assert str(holiday) == holiday.name


@pytest.mark.django_db
class TestGroupModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='test_name')
        return company

    @pytest.fixture
    def branch(self, company):
        branch = Branch.objects.create(
            name='test_name',
            address='test_address',
            company=company,
            phone='932333445',
            about='test_about',
            image='test_image.png'
        )
        return branch

    @pytest.fixture
    def room(self, branch):
        room = Room.objects.create(
            name='test_room',
            branch=branch
        )
        return room

    @pytest.fixture
    def course(self, company):
        course = Course.objects.create(
            name='test_name',
            price=1500,
            description='test_description',
            image='test_image.png',
            lesson_duration=2,
            course_duration=6,
            company=company
        )
        return course

    @pytest.fixture
    def user1(self):
        user1 = User.objects.create_user(
            phone='1233434',
            password='test_password'
        )
        return user1

    @pytest.fixture
    def user2(self):
        user2 = User.objects.create_user(
            phone='12334345',
            password='test_password'
        )
        return user2

    @pytest.fixture
    def group(self, branch, user1, user2, course, room):
        group = Group.objects.create(
            name='test_name',
            days='Odd days',
            status='active',
            room=room,
            teacher=user2,
            start_time=time(hour=9, minute=00),
            end_time=time(hour=12, minute=30),
            course=course,
            branch=branch,
            start_date=date(2023, 2, 23),
            end_date=date(2023, 5, 23),
            tags=['test_tag1', 'tests_tag2', 'tests_tag3'],

        )
        group.students.add(user1)
        return group

    def test_group_model(self, group, user1,user2, branch, course, room):
        assert group.name == 'test_name'
        assert group.days == 'Odd days'
        assert group.status == 'active'
        assert group.room == room
        assert group.start_time == time(hour=9, minute=00)
        assert group.end_time == time(hour=12, minute=30)
        assert group.course == course
        assert group.branch == branch
        assert group.start_date == date(2023, 2, 23)
        assert group.end_date == date(2023, 5, 23)
        assert group.tags == ['test_tag1', 'tests_tag2', 'tests_tag3']

