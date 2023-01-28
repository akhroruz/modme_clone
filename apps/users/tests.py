import pytest
from django.contrib.auth.hashers import make_password

from core.settings import MEDIA_ROOT
from apps.groups.models import Branch
from apps.users.models import User
from apps.users.serializers import UserModelSerializer
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
class TestUserModel:
    @pytest.fixture
    def branches(self):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        branch = Branch.objects.create(
            name='Chilonzor branch',
            address='Chilonzor',
            phone_number='934923326',
            about='hello from',
            image=image,
        )
        return branch

    @pytest.fixture
    def users(self, branches):
        user = User.objects.create(
            full_name='User 1',
            phone='934923327',
            birth='2002-11-27',
            gender='Female',
            branch=branches,
            password=make_password('1234')
        )
        return user

    def test_user_model(self, branches):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        user = User.objects.create(
            full_name='User 1',
            phone='934923327',
            birth='2002-11-27',
            gender=User.GenderChoose.FEMALE,
            photo=image,
            password=make_password('1234')
        )

        assert user.full_name == 'User 1'
        assert user.gender == User.GenderChoose.FEMALE
        assert user.photo is not None

    #
    def test_create_user(self, users, branches):
        serializer = UserModelSerializer(users)
        assert serializer.data['full_name'] == users.full_name
        assert serializer.data['phone'] == int(users.phone)
        assert serializer.data['gender'] == users.gender
        assert serializer.data['birth'] == users.birth
        assert serializer.data['branch'] == branches.pk
        assert len(serializer.data) == 20
