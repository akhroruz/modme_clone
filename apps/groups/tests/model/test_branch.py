import pytest

from groups.models import Company, Branch


@pytest.mark.django_db
class TestBranchModel:
    def test_branch(self):
        company = Company.objects.create(name='Test Company')
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
