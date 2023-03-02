import pytest
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework import status
from rest_framework.reverse import reverse

from groups.models import Room, Holiday
from shared.tests import TestBaseFixture


@pytest.mark.django_db
class TestHolidayModelViewSet(TestBaseFixture):

    def test_list_holiday(self, client, user, holiday):
        client.force_login(user)
        url = reverse('holiday-list') + f'?branch={holiday.branch.pk}'
        response = client.get(url)

        item = response.data['results'][0]
        keys = {'holiday_date', 'branch', 'affect_payment', 'name', 'created_at'}
        assert len(keys.difference(set(item))) == 0  # noqa
        assert response.data['count'] == Holiday.objects.count()
        assert response.status_code == status.HTTP_200_OK

    def test_create_holiday(self, client, user, branch):
        client.force_login(user)
        url = reverse('holiday-list') + f'?branch={branch.pk}'
        data = {
            'holiday_date': '2003-12-12',
            'branch': branch.pk,
            'name': 'Friday',
        }
        previous_count = Holiday.objects.count()
        response = client.post(url, data, 'application/json')
        assert previous_count + 1 == Holiday.objects.count()

        item = response.json()
        keys = {'holiday_date', 'branch', 'name'}
        assert len(keys.difference(set(item))) == 0  # noqa
        assert data == item
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_holiday(self, client: Client, user, holiday):
        client.force_login(user)
        url = reverse('holiday-detail', args=(holiday.pk,)) + f'?branch={holiday.branch.pk}'
        data = {
            'holiday_date': '1999-12-10',
            'branch': holiday.branch.pk,
            'name': 'Sunday',
        }

        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        item = response.json()
        keys = {'name', 'branch', 'holiday_date'}
        assert len(keys.difference(set(item))) == 0  # noqa
        assert data == item
        assert response.status_code == status.HTTP_200_OK

    def test_delete_holiday(self, client: Client, user, holiday):
        client.force_login(user)
        url = reverse('holiday-detail', args=(holiday.pk,)) + f'?branch={holiday.branch.pk}'
        previous_count = Holiday.objects.count()
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert previous_count - 1 == Room.objects.count()
