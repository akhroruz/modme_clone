import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from groups.models import Branch
from shared.tests import TestBaseFixture
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa


@pytest.mark.django_db
class TestBranchModelViewSet(TestBaseFixture):
    def test_branch_list(self, user, client: Client, branch, company):
        keys = {'id', 'name'}
        client.force_login(user)
        url = reverse('branch-list') + f'?company={company.pk}'
        response = client.get(url)  # noqa
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == Branch.objects.count()
        item = response.data['results'][0]
        assert len(keys.difference(set(item))) == 0  # noqa

    def test_create_branch(self, user, client, company):
        client.force_login(user)
        data = {
            'name': 'test_branch',
            'address': 'test_address',
            'phone': '911993234',
            'about': 'test_about',
            'company': company.pk

        }
        url = reverse('branch-list') + f'?company={company.pk}'
        pre_count = Branch.objects.count()
        response = client.post(url, data)
        item = response.json()
        keys = {'name', 'address', 'company', 'phone', 'about'}
        assert len(keys.difference(set(item))) == 0  # noqa
        assert pre_count + 1 == Branch.objects.count()
        item.pop('image', None)
        assert data == item
        assert response.status_code == status.HTTP_201_CREATED

    def test_update__branch(self, client, user, branch, company):
        client.force_login(user)
        data = {'name': 'test_branch',
                'address': 'test_address',
                'phone': '911993234',
                'about': 'test_about',
                'company': company.pk
                }
        url = reverse('branch-detail', args=(branch.pk,)) + f'?company={company.pk}'
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)

        keys = {
            'name', 'address', 'phone', 'about', 'company'
        }
        item = response.json()
        item.pop('image', None)
        assert len(keys.difference(set(item))) == 0  # noqa
        assert item == data

    def test_partial_update_branch(self, client, user, branch, company):
        client.force_login(user)  # noqa
        data = {
            'address': 'test_address',
            'about': 'test_about',
            'company': company.pk
        }
        url = reverse('branch-detail', args=(branch.pk,)) + f'?company={company.pk}'
        response = client.patch(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)

        keys = {
            'address', 'about', 'company'
        }
        item = response.json()
        item.pop('image', None)
        assert len(keys.difference(set(item))) == 0  # noqa
        for key, value in data.items():
            assert item[key] == value
        assert response.status_code == status.HTTP_200_OK

    def test_delete_branch(self, client, user, branch, company):
        client.force_login(user)
        url = reverse('branch-detail', args=(branch.pk,)) + f'?company={company.pk}'
        pre_count = Branch.objects.count()
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert pre_count - 1 == Branch.objects.count()
