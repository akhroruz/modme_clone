import pytest

from apps.users.models import User
from core.settings import MEDIA_ROOT


@pytest.mark.django_db
class TestUserModel:
    @pytest.fixture
    def users(self, db, client):
        user = User.objects.create(
            full_name='User 1',
            phone='934923327',
            birth='2002-11-27',
            gender='Female',
            password='1234'
        )
        return user

    def test_user_model(self):
        print(1111111111111111111111111111111111111111111111111111111111111111)
        from django.core.files.uploadedfile import SimpleUploadedFile
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        user = User.objects.create(
            full_name='User 1',
            phone='934923327',
            birth='2002-11-27',
            gender=User.GenderChoose.FEMALE,
            photo=image,
            password='1234'
        )

        assert user.full_name == 'User 1'
        assert user.gender == User.GenderChoose.FEMALE
        print(user.photo.url)
    #
    # def test_create_user(self, users):
    #     name = 'User 1'
    #     count = User.objects.count()
    #     User.objects.create(
    #         full_name=name,
    #         phone='934923328',
    #         birth='2002-11-28',
    #         gender='Female',
    #         photo='media/default.jpg',
    #     )
    #     assert users.full_name == name
    #     assert User.objects.count() - 1 == count
