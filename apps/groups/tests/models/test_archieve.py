from datetime import time

import pytest

from groups.models import Company
from groups.models import ArchiveReason


@pytest.mark.django_db
class TestArchiveModel:

    def test_create_archive(self):
        company_data = {
            'name': 'PDP',
            'logo': 'test_logo.png',
            'colors': 'Red',
            'start_working_time': time(hour=9, minute=00),
            'end_working_time': time(hour=12, minute=00),
            'phone': '991212334',
            'company_oferta': 'test_logo.png'
        }
        company = Company.objects.create(**company_data)
        data = {
            'name': 'PDP',
            'company': company
        }
        count = ArchiveReason.objects.count()
        archive = ArchiveReason.objects.create(**data)
        assert archive.name == data['name']
        assert count + 1 == ArchiveReason.objects.count()
