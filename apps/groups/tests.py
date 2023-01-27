import pytest

from apps.groups.models import Course, Role, Branch, Weekend, Room, Group
from users.models import User


@pytest.mark.django_db
class TestRoleModel:

    @pytest.fixture
    def role(self):
        role = Role.objects.create(name='Teacher')
        return role

    def test_role_create_model(self, role):
        name = 'CEO'
        count = Role.objects.count()
        role = Role.objects.create(name=name)
        assert Role.objects.count() - 1 == count
        assert role.name == name


@pytest.mark.django_db
class TestCourse:

    @pytest.fixture
    def course(self):
        course = Course.objects.create(name='course_en', price=1)
        return course

    def test_course_create_model(self, course):
        name = 'course_ru'
        price = 2
        count = Course.objects.count()
        course = Course.objects.create(name=name, price=price)
        assert Course.objects.count() - 1 == count
        assert name == course.name
        assert price == course.price


@pytest.mark.django_db
class TestBranch:
    @pytest.fixture
    def branch(self):
        branch = Branch.objects.create(name='branch', address='Uzb', phone_number=993993233, about='big description',
                                       image='fa.jpg')
        return branch

    def test_branch_create_model(self, branch):
        name = 'branches 1'
        address = 'AZZ'
        phone_number = 181818
        about = 'small description'
        image = 'fa2.jpg'
        count = Branch.objects.count()
        branch = Branch.objects.create(name=name, address=address, phone_number=phone_number, about=about, image=image)
        assert Branch.objects.count() - 1 == count
        assert name == branch.name
        assert address == branch.address
        assert phone_number == branch.phone_number
        assert about == branch.about
        assert image == branch.image


@pytest.mark.django_db
class TestRoom:
    @pytest.fixture
    def room(self):
        room = Room.objects.create(name='Apple')
        return room

    def test_room_create_model(self, room):
        name = 'Cisco'
        count = Room.objects.count()
        room = Room.objects.create(name=name)
        assert Room.objects.count() - 1 == count
        assert name == room.name


@pytest.mark.django_db
class TestWeekend:
    @pytest.fixture
    def weekend(self):
        weekend = Weekend.objects.create(name='Monday', affects_payment=False)
        return weekend

    def test_weekend_create_model(self, weekend):
        name = 'Sunday'
        affects_payment = True
        count = Weekend.objects.count()
        weekend = Weekend.objects.create(name=name, affects_payment=affects_payment)
        assert Weekend.objects.count() - 1 == count
        assert name == weekend.name
        assert affects_payment == weekend.affects_payment


@pytest.mark.django_db
class TestGroup:
    @pytest.fixture
    def users(self):
        user = User.objects.create(name='Teacher')
        return user

    @pytest.fixture
    def groups(self, users):
        group = Group.objects.create(name='Java', days='add_days', teacher=users.pk)
        return group

    def test_group_create_model(self, groups, users):
        name = 'Python'
        days = 'even_days'
        room = 'Cisco'
        count = Group.objects.count()
        group = Group.objects.create(name=name, days=days, room=room, teacher=users.pk)
        assert Group.objects.count() - 1 == count
        assert name == group.name
        assert days == group.days
        assert room == group.room
