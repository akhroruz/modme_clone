from datetime import time

import pytest  # noqa

from groups.models import Company


@pytest.mark.django_db
class TestCompanyModel:
    def test_create_company(self):  # noqa
        data = {
            'name': 'PDP',
            'logo': 'test_logo.png',
            'colors': 'Red',
            'start_working_time': time(hour=9, minute=00),
            'end_working_time': time(hour=12, minute=00),
            'phone': '991212334',
            'company_oferta': 'test_logo.png'
        }
        company_count = Company.objects.count()
        company = Company.objects.create(**data)
        assert company.name == data['name']
        assert company.logo == data['logo']
        assert company.colors == data['colors']
        assert company.start_working_time == data['start_working_time']
        assert company.end_working_time == data['end_working_time']
        assert company.phone == data['phone']
        assert company.company_oferta == data['company_oferta']
        assert str(company) == company.name
        assert company_count + 1 == Company.objects.count()
