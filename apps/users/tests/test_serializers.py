import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.groups.models import Branch
from apps.groups.models import Holiday
from core.settings import MEDIA_ROOT
from groups.serializers import HolidayListModelSerializer


@pytest.mark.django_db
class TestModelSerializer:
    @pytest.fixture
    def branches(self):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        branch = Branch.objects.create(
            name='Branch 1',
            address='Address 1',
            phone=934923327,
            about='Test',
            image=image
        )
        return branch

    @pytest.fixture
    def holidays(self, branches):
        holiday = Holiday.objects.create(
            name='Name 1',
            branch_id=branches.uuid,
            holiday_date='2021-12-12',
            affect_payment=True
        )
        return holiday

    def test_holiday_serializer(self, branches, holidays):
        serializer = HolidayListModelSerializer(holidays)
        assert serializer.data['branch'] == holidays.branch.uuid
        assert serializer.data['holiday_date'] == holidays.holiday_date
        assert serializer.data['affect_payment'] == holidays.affect_payment
        assert serializer.data['name'] == holidays.name
        assert len(serializer.data) == 5

# @pytest.mark.django_db
# class TestUserModel:
#     @pytest.fixture
#     def branches(self):
#         image_path = MEDIA_ROOT + '/test.png'
#         image = SimpleUploadedFile('test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
#
#         branch = Branch.objects.create(
#             name='Chilonzor branch',
#             address='Chilonzor',
#             phone_number='934923326',
#             about='hello from',
#             image=image,
#         )
#         return branch
#
#     @pytest.fixture
#     def users(self, branches):
#         user = User.objects.create(
#             full_name='User 1',
#             phone='934923327',
#             birth='2002-11-27',
#             gender='Female',
#             branch=branches,
#             password=make_password('1234')
#         )
#         return user
#
#     def test_user_model(self, branches):
#         image_path = MEDIA_ROOT + '/test.png'
#         image = SimpleUploadedFile('test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
#
#         user = User.objects.create(
#             full_name='User 1',
#             phone='934923327',
#             birth='2002-11-27',
#             gender=User.GenderChoose.FEMALE,
#             photo=image,
#             password=make_password('1234')
#         )
#
#         assert user.full_name == 'User 1'
#         assert user.gender == User.GenderChoose.FEMALE
#         assert user.photo is not None
#
#     #
#     def test_create_user(self, users, branches):
#         serializer = UserModelSerializer(users)
#         assert serializer.data['full_name'] == users.full_name
#         assert serializer.data['phone'] == int(users.phone)
#         assert serializer.data['gender'] == users.gender
#         assert serializer.data['birth'] == users.birth
#         assert serializer.data['branch'] == branches.pk
#         assert len(serializer.data) == 21
