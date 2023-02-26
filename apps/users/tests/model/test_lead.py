import pytest
from users.models import LeadIncrement, Lead


@pytest.mark.django_db
class TestLeadIncrementModel:
    def test_lead_increment(self):
        data = {'name': 'test_name'}
        lead_increment = LeadIncrement.objects.create(**data)
        assert lead_increment.name == data['name']
        assert str(lead_increment) == lead_increment.name


@pytest.mark.django_db
class TestLeadModel:
    def test_lead(self):
        lead_increment = LeadIncrement.objects.create(name='test_name')
        data = {
            'full_name': 'test_fullname',
            'comment': 'test_comment',
            'phone': 934492123,
            'status': 'Requests',
            'lead_increment': lead_increment
        }
        count = Lead.objects.count()
        lead = Lead.objects.create(**data)
        assert lead.full_name == data['full_name']
        assert lead.comment == data['comment']
        assert lead.phone == data['phone']
        assert lead.status == data['status']
        assert lead.lead_increment == data['lead_increment']
        assert str(lead) == f'{lead.full_name} | {lead.phone}'
        assert count + 1 == Lead.objects.count()
