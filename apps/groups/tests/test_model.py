from datetime import date, time
import pytest

from groups.models import Company, Branch, Room, Course, Holiday, Group
from users.models import User


@pytest.mark.django_db
class TestCompanyModel:
    def test_company(self):
        company_data = {
            'name': 'PDP'
        }
        company_count = Company.objects.count()
        company = Company.objects.create(**company_data)
        assert company.name == company_data['name']
        assert str(company) == company.name
        assert company_count + 1 == Company.objects.count()


@pytest.mark.django_db
class TestBranchModel:
    def test_branch(self):
        company_data = {
            'name': 'Test Company'
        }
        company = Company.objects.create(**company_data)
        branch_data = {
            'name': 'Test Branch',
            'address': 'Test Address',
            'company': company,
            'phone': '949343943',
            'about': 'Test About',
            'image': 'test_image.png'
        }
        branch_count = Branch.objects.count()
        branch = Branch.objects.create(**branch_data)
        assert branch.name == 'Test Branch'
        assert branch.address == 'Test Address'
        assert branch.phone == '949343943'
        assert branch.about == 'Test About'
        assert branch.image == 'test_image.png'
        assert str(branch) == branch.name
        assert str(company) == company.name
        assert branch.company.name == 'Test Company'
        assert branch_count + 1 == Branch.objects.count()


@pytest.mark.django_db
class TestRoomModel:

    def test_room(self):
        company_data = {
            'name': 'PDP'
        }
        company = Company.objects.create(**company_data)
        branch_data = {
            'name': 'test branch',
            'address': 'test branch address',
            'company': company,
            'phone': '934341245',
            'about': 'test branch about',
            'image': 'branch_image.png'
        }
        branch = Branch.objects.create(**branch_data)
        room_count = Room.objects.count()
        room = Room.objects.create(
            name='test_name',
            branch=branch
        )

        assert room.name == 'test_name'
        assert room.branch == branch
        assert str(room) == room.name
        assert room_count == Room.objects.count() - 1


@pytest.mark.django_db
class TestCourseModel:
    def test_create_course(self):
        company_data = {
            'name': 'test_name'
        }
        company = Company.objects.create(**company_data)

        course_data = {
            'name': 'test_name',
            'price': 500,
            'description': 'test_description',
            'image': 'test_image.png',
            'lesson_duration': 3,
            'course_duration': 6,
            'company': company
        }
        course_count = Course.objects.count()
        course = Course.objects.create(**course_data)
        assert course.name == 'test_name'
        assert course.price == 500
        assert course.description == 'test_description'
        assert course.image == 'test_image.png'
        assert course.lesson_duration == 3
        assert course.course_duration == 6
        assert course.company == company
        assert str(course) == course.name
        assert course_count == Company.objects.count() - 1


@pytest.mark.django_db
class TestHolidayModel:
    def test_holiday(self):
        company_data = {
            'name': 'test_company'
        }
        company = Company.objects.create(**company_data)  # noqa

        branch_data = {
            'name': 'test_name',
            'address': 'test_address',
            'company': company,
            'phone': '933432343',
            'about': 'test_about',
            'image': 'test_image.png',
        }
        branch = Branch.objects.create(**branch_data)
        holiday_data = {
            'name': 'test_name',
            'holiday_date': date(2023, 12, 25),
            'affect_payment': False,
            'branch': branch
        }

        holiday_count = Holiday.objects.count()
        holiday = Holiday.objects.create(**holiday_data)

        assert holiday.name == 'test_name'
        assert holiday.holiday_date == date(2023, 12, 25)
        assert not holiday.affect_payment
        assert branch == branch
        assert str(holiday) == holiday.name
        assert holiday_count + 1 == Holiday.objects.count()


@pytest.mark.django_db
class TestGroupModel:
    def test_group(self):
        company_data = {
            'name': 'test_company'
        }
        company = Company.objects.create(**company_data)
        branch_data = {
            'name': 'test_name',
            'address': 'test_address',
            'company': company,
            'phone': '933432343',
            'about': 'test_about',
            'image': 'test_image.png',
        }
        branch = Branch.objects.create(**branch_data)

        room_data = {
            'name': 'test_room',
            'branch': branch
        }
        room = Room.objects.create(**room_data)

        course_data = {
            'name': 'test_name',
            'price': 1500,
            'description': 'test_description',
            'image': 'test_image.png',
            'lesson_duration': 2,
            'course_duration': 6,
            'company': company
        }
        course = Course.objects.create(**course_data)

        user_data = {
            'phone': '1233434',
            'password': 'test_password'
        }
        user = User.objects.create_user(**user_data)

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
        assert group.tags == ['test_tag1']
        assert group_count + 1 == Group.objects.count()
