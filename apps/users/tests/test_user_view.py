import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as Role
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
from rest_framework import status
from rest_framework.reverse import reverse

from core.settings import MEDIA_ROOT
from groups.models import Group, Room
from shared.tests import TestBaseFixture
from users.models import User


# TODO Ustozga with image, from ahror oka
@pytest.mark.django_db
class TestUserModelViewSet(TestBaseFixture):

    @pytest.fixture
    def create_group(self, faker, branch):
        room = Room.objects.create(name=faker.first_name(), branch=branch)
        group = Group.objects.create(
            name='new_group',
            days=Group.DaysChoice.ODD_DAYS,
            room=room,
            branch=branch.pk,
            tags=['tag1', 'tag2']
        )
        return group

    @pytest.fixture
    def role(self):
        role = Role.objects.create(
            name='teacher'
        )
        return role

    @pytest.fixture
    def user(self, archive, role, branch):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        user = User.objects.create_user(
            phone='8888888',
            gender=User.GenderChoose.MALE,
            birth_date='2003-12-01',
            photo=image,
            first_name='jack',
            password='1',
            data={}
        )

        user.role.add(role)
        user.branch.add(branch)
        user.save()
        return user

    def test_user_list(self, client, user, branch, role):
        client.force_login(user)
        url = '%s?branch=%s&user_type=%s' % (reverse('user-list'), branch.pk, role.name)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert User.objects.count() == response.data['count']

    def test_create_user(self, client, user, archive, branch, role):
        client.force_login(user)
        data = {
            'phone': '8888889',
            'gender': user.GenderChoose.MALE,
            'birth_date': '2003-12-01',
            'role': role,
            'first_name': 'jack',
            'password': '1',
        }
        url = '%s?branch=%s&user_type=%s' % (reverse('user-list'), branch.pk, role.name)
        count = User.objects.count()
        response = client.post(url, data)
        x = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        keys = {'first_name', 'phone', 'gender', 'birth_date'}
        for key in keys:
            assert data[key] == x[key]
        assert count + 1 == User.objects.count()

    # def test_update_user(self, client: Client, user, branch, role):
    #     client.force_login(user)
    #     image_path = MEDIA_ROOT + '/test.png'
    #     image = SimpleUploadedFile('test.png', open(image_path, 'rb').read(), 'image/png')
    #     data = {
    #         'gender': User.GenderChoose.FEMALE,
    #         'birth_date': '1999-10-10',
    #         'photo': image,
    #         'password': '1',
    #     }
    #
    #     url = reverse('user-detail', args=(user.pk,)) + f'?branch={branch.pk}&user_type={role.name}'
    #     response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
    #     assert response.status_code == status.HTTP_200_OK
    #     x = response.json()
    #     keys = {'gender', 'birth_date', 'full_name'}
    #     for key in keys:
    #         assert data[key] == x[key]

    def test_patch_user(self, client: Client, user, branch, role):
        client.force_login(user)
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', open(image_path, 'rb').read(), 'image/png')
        data = {
            'birth_date': '1000-10-10',
            'password': 'password1',
            'role': role.pk,
            'photo': image,
            'gender': user.GenderChoose.MALE
        }

        url = reverse('user-detail', args=(user.pk,)) + f'?branch={branch.pk}&user_type={role.name}'
        response = client.patch(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        keys = 'birth_date', 'gender'
        for key in keys:
            assert data[key] == response.data[key]
        assert response.status_code == status.HTTP_200_OK

    def test_delete_user(self, client: Client, user, branch, role, company):
        client.force_login(user)
        url = reverse('user-detail', args=(user.pk,)) + f'?branch={branch.pk}&user_type={role.name}'
        count = get_user_model().objects.count()
        response = client.delete(url)
        assert get_user_model().objects.count() + 1 == count
        assert response.status_code == status.HTTP_204_NO_CONTENT
