import pytest
from datetime import time

from django.core.files.uploadedfile import SimpleUploadedFile

from core.settings import MEDIA_ROOT
from groups.models import Company, Branch


@pytest.mark.django_db
class TestBranchModel:
    def test_branch(self):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        company_data = {
            'name': 'PDP',
            'logo': image,
            'colors': 'Red',
            'start_working_time': time(hour=9, minute=00),
            'end_working_time': time(hour=12, minute=00),
            'phone': '991212334',
            'company_oferta': image

        }
        company = Company.objects.create(**company_data)
        data = {
            'name': 'Test Branch',
            'address': 'Test Address',
            'company': company,
            'phone': '949343943',
            'about': 'Test About',
            'image': image
        }
        branch_count = Branch.objects.count()
        branch = Branch.objects.create(**data)
        assert branch.name == data['name']
        assert branch.address == data['address']
        assert branch.phone == data['phone']
        assert branch.about == data['about']
        assert str(branch) == branch.name
        assert str(company) == company.name
        assert branch.company.name == company_data['name']
        assert branch_count + 1 == Branch.objects.count()
