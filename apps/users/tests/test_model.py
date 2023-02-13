import pytest
from users.models import Lead, LeadIncrement


@pytest.mark.django_db
class TestLeadModel:

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

    def test_lead_fields(self, lead):
        lead = Lead.objects.get(id=lead.id)
        assert lead.full_name == lead.full_name
        assert lead.comment == lead.comment
        assert lead.phone == lead.phone
        assert lead.status == lead.status
        assert lead.lead_increment.pk == lead.lead_increment_id


@pytest.mark.django_db
class TestLeadIncrementModel:
    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead 1'
        )
        return lead_increment

    def test_lead_increment_name(self, lead_increment):
        lead_increment = LeadIncrement.objects.get(id=lead_increment.id)
        assert lead_increment.name == lead_increment.name
