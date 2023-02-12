import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from django.test import Client
from users.models import Lead
from users.models import LeadIncrement


@pytest.mark.django_db
class TestLeadModelViewSet:

    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead 1'
        )
        return lead_increment

    @pytest.fixture
    def lead(self, lead_increment):
        return Lead.objects.create(
            full_name='full name 1',
            comment='comment 1',
            phone=990675624,
            status=Lead.LeadStatus.REQUESTS,
            lead_increment=lead_increment
        )

    def test_list_lead(self, client: Client, lead):
        url = reverse('lead-list')
        response = client.get(url)
        item = response.data['results'][0]
        assert response.status_code == status.HTTP_200_OK
        assert item['full_name'] == lead.full_name
        assert item['comment'] == lead.comment
        assert item['phone'] == lead.phone
        assert item['status'] == lead.status
        assert item['lead_increment'] == lead.lead_increment_id

    def test_create_lead(self, client: Client, lead):
        url = reverse('lead-list')
        data = {
            'full_name': lead.full_name,
            'comment': lead.comment,
            'phone': lead.phone,
            'status': lead.status,
            'lead_increment': lead.lead_increment_id
        }
        response = client.post(url, data, 'application/json')
        item = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert item['full_name'] == data['full_name']
        assert item['comment'] == data['comment']
        assert item['phone'] == data['phone']
        assert item['status'] == data['status']
        assert item['lead_increment'] == data['lead_increment']

    def test_update_lead(self, client: Client, lead):
        url = reverse('lead-detail', args=[lead.id])
        data = {
            'full_name': lead.full_name,
            'comment': lead.comment,
            'phone': lead.phone,
            'status': lead.status,
            'lead_increment': lead.lead_increment_id
        }
        response = client.put(url, data, 'application/json')
        item = response.data

        assert response.status_code == status.HTTP_200_OK
        assert item['full_name'] == data['full_name']
        assert item['comment'] == data['comment']
        assert item['phone'] == data['phone']
        assert item['status'] == data['status']
        assert item['lead_increment'] == data['lead_increment']

    def test_delete_lead(self, client: Client, lead):
        url = reverse('lead-detail', args=[lead.id])
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestLeadIncrementModelVIewSet:

    @pytest.fixture
    def lead_increment(self):
        return LeadIncrement.objects.create(
            name='Lead Increment 1'
        )

    def test_list_lead_increment(self, client: Client, lead_increment):
        url = reverse('lead_increment-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['results'][0]['name'] == lead_increment.name

    def test_create_lead_increment(self, client: Client, lead_increment):
        url = reverse('lead_increment-list')
        data = {
            'name': 'Lead Increment 1'
        }
        response = client.post(url, data, 'application/json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == lead_increment.name

    def test_update_lead_increment(self, client: Client, lead_increment):
        url = reverse('lead_increment-detail', args=[lead_increment.id])
        data = {
            'name': 'Lead Increment 1'
        }
        response = client.put(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == lead_increment.name

    def test_delete_lead_increment(self, client: Client, lead_increment):
        url = reverse('lead_increment-detail', args=[lead_increment.id])
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
