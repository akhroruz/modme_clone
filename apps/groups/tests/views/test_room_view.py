import pytest
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework import status
from rest_framework.reverse import reverse

from groups.models import Branch, Room
from shared.tests import TestBaseFixture


@pytest.mark.django_db
class TestRoomModelViewSet(TestBaseFixture):

    def test_list_room(self, client, user, room):
        client.force_login(user)
        url = reverse('room-list') + f'?branch={room.branch.pk}'
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == Room.objects.count()
        item = response.data['results'][0]
        keys = {'name', 'id'}
        assert len(keys.difference(set(item))) == 0  # noqa
        assert item['name'] == room.name

    def test_create_room(self, client, room, user):
        client.force_login(user)
        url = reverse('room-list') + f'?branch={room.branch.pk}'
        data = {
            'name': 'Room Created 2',
            'branch': room.branch.pk,
        }
        previous_count = Branch.objects.count()
        response = client.post(url, data, 'application/json')
        assert previous_count + 1 == Room.objects.count()

        item = response.json()
        keys = {'name', 'branch'}
        assert len(keys.difference(set(item))) == 0  # noqa
        for key, value in data.items():
            assert item[key] == value
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_room(self, client: Client, room, user):
        client.force_login(user)
        url = reverse('room-detail', args=(room.pk,)) + f'?branch={room.branch.pk}'
        data = {
            'name': 'New updated Room 1',
            'branch': room.branch.pk,
        }

        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        assert response.status_code == status.HTTP_200_OK

        item = response.json()
        keys = {'name', 'branch'}
        assert len(keys.difference(set(item))) == 0  # noqa
        assert data == item

    def test_delete_room(self, client: Client, room, user):
        client.force_login(user)
        url = reverse('room-detail', args=(room.pk,)) + f'?branch={room.branch.pk}'
        previous_count = Room.objects.count()
        response = client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert previous_count - 1 == Room.objects.count()
