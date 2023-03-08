import pytest
from datetime import time

from groups.models import Company, Branch


@pytest.mark.django_db
class TestBranchModel:
    def test_branch(self):
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
            'name': 'Test Branch',
            'address': 'Test Address',
            'company': company,
            'phone': '949343943',
            'about': 'Test About',
            'image': 'test_image.png'
        }
        branch_count = Branch.objects.count()
        branch = Branch.objects.create(**data)
        assert branch.name == data['name']
        assert branch.address == data['address']
        assert branch.phone == data['phone']
        assert branch.about == data['about']
        assert branch.image == data['image']
        assert str(branch) == branch.name
        assert str(company) == company.name
        assert branch.company.name == 'Test Company'
        assert branch_count + 1 == Branch.objects.count()
