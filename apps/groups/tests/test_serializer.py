from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.groups.models import Role
from apps.groups.serializers import RoleModelSerializer
from apps.groups.models import Branch
from apps.groups.serializers import BranchModelSerializer
from core.settings import MEDIA_ROOT
from apps.groups.models import Room
from apps.groups.serializers import RoomModelSerializer
from apps.groups.models import Course
from apps.groups.serializers import CourseModelSerializer, WeekendModelSerializer, GroupModelSerializer
from apps.groups.models import Weekend, Group
from apps.users.models import User


@pytest.mark.django_db
class TestRoleModelSerializer:

    @pytest.fixture
    def role_fixture(self):
        return Role.objects.create(name='Role 1')

    def test_role_model_serializer(self, role_fixture):
        serializer = RoleModelSerializer(role_fixture)
        assert serializer.data['name'] == role_fixture.name


def temporary_image():
    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'png')
    return SimpleUploadedFile("media/images/test.png", bts.getvalue())


@pytest.mark.django_db
class TestBranchModelSerializer:
    @pytest.fixture
    def branch_fixture(self):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        return Branch.objects.create(
            name='Branch 1',
            address='Address 1',
            phone_number=990675624,
            about='Text 1',
            image=image
        )

    def test_branch_model_serializer(self, branch_fixture):
        serializer = BranchModelSerializer(branch_fixture)
        assert serializer.data['name'] == branch_fixture.name
        assert serializer.data['address'] == branch_fixture.address
        assert serializer.data['phone_number'] == branch_fixture.phone_number
        assert serializer.data['about'] == branch_fixture.about
        assert serializer.data['image'] == branch_fixture.image.url


@pytest.mark.django_db
class TestRoomModelSerializer:
    @pytest.fixture
    def room_fixture(self):
        return Room.objects.create(name='Room 1')

    def test_room_model_serializer(self, room_fixture):
        serializer = RoomModelSerializer(room_fixture)
        assert serializer.data['name'] == room_fixture.name


@pytest.mark.django_db
class TestCourseModelSerializer:
    @pytest.fixture
    def course_fixture(self):
        return Course.objects.create(
            name='Course 1',
            price='10.00'
        )

    def test_course_model_serializer(self, course_fixture):
        serializer = CourseModelSerializer(course_fixture)
        assert serializer.data['name'] == course_fixture.name
        assert serializer.data['price'] == course_fixture.price


@pytest.mark.django_db
class TestWeekendModelSerializer:
    @pytest.fixture
    def weekend_fixture(self):
        return Weekend(
            name='Wednesday',
            weekend_day='2022-10-10',
            affects_payment=True
        )

    def test_weekend_model_serializer(self, weekend_fixture):
        serializer = WeekendModelSerializer(weekend_fixture)
        assert serializer.data['name'] == weekend_fixture.name
        assert serializer.data['weekend_day'] == weekend_fixture.weekend_day
        assert serializer.data['affects_payment'] == weekend_fixture.affects_payment


@pytest.mark.django_db
class TestGroupModelSerializer:
    @pytest.fixture
    def room_fixture(self):
        room = Room.objects.create(name='Room 1')
        return room

    @pytest.fixture
    def user_fixture(self, db, client):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        user = User.objects.create(
            full_name='User 1',
            phone='934923327',
            birth='2002-11-27',
            gender='Female',
            photo=image,
            password='1234'
        )
        return user

    @pytest.fixture
    def group_fixture(self, user_fixture, room_fixture):
        group = Group.objects.create(
            name='Group 1',
            days=Group.DaysChoice.DAY_OFF,
            room_id=room_fixture.uuid,
            # teacher_id=user_fixture.pk,
            start_time='18:11:12',
            group_time='2022-10-10'
        )
        return group

    def test_group_model_serializer(self, group_fixture, user_fixture, room_fixture):
        serializer = GroupModelSerializer(group_fixture)
        assert serializer.data['name'] == group_fixture.name
        assert serializer.data['days'] == group_fixture.DaysChoice.DAY_OFF
        assert serializer.data['room'] == room_fixture.uuid
        # assert serializer.data['teacher'] == user_fixture.role
        assert serializer.data['start_time'] == group_fixture.start_time
        assert serializer.data['group_time'] == group_fixture.group_time
