import pytest

from users.models import Lead, LeadIncrement
from users.serializers import LeadModelSerializer, LeadIncrementModelSerializer


@pytest.mark.django_db
class TestLeadModelSerializer:
    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead Increment 1'
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

    def test_create_lead_model_serializer(self, lead):
        serializer = LeadModelSerializer(lead)
        assert serializer.data['full_name'] == lead.full_name
        assert serializer.data['comment'] == lead.comment
        assert serializer.data['phone'] == lead.phone
        assert serializer.data['status'] == lead.status
        assert serializer.data['lead_increment'] == lead.lead_increment_id

    def test_delete_lead_model_serializer(self, lead):
        lead.delete()
        assert not Lead.objects.filter(pk=lead.pk).exists()


@pytest.mark.django_db
class TestLeadIncrementModelSerializer:
    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead Increment 1'
        )
        return lead_increment

    def test_create_lead_increment_model_serializer(self, lead_increment):
        serializer = LeadIncrementModelSerializer(lead_increment)
        assert serializer.data['name'] == lead_increment.name

    def test_delete_lead_increment_model_serializer(self, lead_increment):
        lead_increment.delete()
        assert not LeadIncrement.objects.filter(pk=lead_increment.pk).exists()
