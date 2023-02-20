import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework import status
from rest_framework.reverse import reverse

from core.settings import MEDIA_ROOT
from groups.models import Branch, Company, Room
from users.models import User


@pytest.mark.django_db
class TestBranchModelViewSet:

    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='Company 1')
        return company

    @pytest.fixture
    def branch(self, company):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        branch = Branch.objects.create(
            name='Branch 1',
            address='Uzbekistan, Toshkent',
            phone='12345678',
            about='Smth about this branch',
            company=company,
            image=image

        )
        return branch

    def test_list_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-list'), branch.company.pk)
        response = client.get(url)
        item = response.data['results'][0]
        # json.loads(response.content) == response.data     # ishlatib korish kere shunaqa stildi
        assert response.status_code == status.HTTP_200_OK
        assert item['name'] == branch.name
        assert item['address'] == branch.address
        assert item['phone'] == branch.phone
        assert item['about'] == branch.about
        assert item['company'] == branch.company.pk

    def test_create_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-list'), branch.company.id)
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        data = {
            'name': branch.name,
            'address': branch.address,
            'phone': '987654321',
            'about': branch.about,
            'company': branch.company.pk,
            'image': image
        }
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        item = response.json()
        assert item['name'] == data['name']
        assert item['address'] == data['address']
        assert item['phone'] == data['phone']
        assert item['about'] == data['about']
        assert item['company'] == data['company']

    def test_retrieve_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-detail', args=[branch.id]), branch.company.id)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        item = response.data
        assert item['name'] == branch.name
        assert item['address'] == branch.address
        assert item['phone'] == branch.phone
        assert item['about'] == branch.about
        assert item['company'] == branch.company.pk

    def test_update_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-detail', args=[branch.id]), branch.company.id)
        data = {
            'name': 'New updated Branch 1',
            'address': 'dsadas',
            'phone': '11111111',
            'about': branch.about,
            'company': branch.company.pk,
            'image': branch.image,
        }
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        assert response.status_code == status.HTTP_200_OK
        item = response.data
        assert item['name'] == data['name']
        assert item['address'] == data['address']
        assert item['phone'] == data['phone']
        assert item['about'] == data['about']
        assert item['company'] == data['company']

    def test_delete_branch(self, client: Client, branch):
        url = '%s?company=%s' % (reverse('branch-detail', args=[branch.id]), branch.company.id)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestRoomModelViewSet:

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone='123654987', password='Asdvbn12ghnf115dfsa2f', is_superuser=True,
                                        is_staff=True)
        return user

    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='Company 1')
        return company

    @pytest.fixture
    def branch(self, company):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        branch = Branch.objects.create(
            name='Room 1',
            address='Uzbekistan, Toshkent',
            phone='12345678',
            about='Smth about this branch',
            company=company,
            image=image
        )
        return branch

    @pytest.fixture
    def room(self, branch):
        room = Room.objects.create(name='Room 1', branch=branch)
        return room

    def test_list_room(self, client: Client, room, user):
        client.force_login(user)
        url = reverse('room-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        item = response.data['results'][0]
        assert item['id'] == room.id
        assert item['name'] == room.name
        assert item['branch'] == room.branch.pk

    def test_create_room(self, client: Client, room, user):
        client.force_login(user)
        url = reverse('room-list')
        data = {
            'name': 'Room 2',
            'branch': room.branch.pk,
        }

        response = client.post(url, data, 'application/json')
        assert response.status_code == status.HTTP_201_CREATED

        item = response.json()
        assert item['name'] == data['name']
        assert item['branch'] == data['branch']

    def test_retrieve_room(self, client: Client, room, user):
        client.force_login(user)
        url = reverse('room-detail', args=[room.id])
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        item = response.data
        assert item['name'] == room.name
        assert item['branch'] == room.branch.pk

    def test_update_room(self, client: Client, room, user):
        client.force_login(user)
        url = reverse('room-detail', args=[room.id])
        data = {
            'name': 'New updated Room 1',
            'branch': room.branch.pk,
        }
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        assert response.status_code == status.HTTP_200_OK

        item = response.data
        assert item['name'] == data['name']
        assert item['branch'] == data['branch']

    def test_delete_room(self, client: Client, room, user):
        client.force_login(user)
        url = reverse('room-detail', args=[room.id])
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT