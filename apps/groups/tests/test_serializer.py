import pytest

from groups.models import Company
from groups.serializers import CompanyModelSerializer, BranchModelSerializer


@pytest.mark.django_db
class TestCompanySerializer:

    def test_company_serializer_valid(self):
        data = {
            'name': 'Gexpert',
        }
        serializer = CompanyModelSerializer(data=data)
        assert serializer.is_valid()
        assert serializer.validated_data == data

    def test_company_serializer_create(self):
        company_data = {
            'name': 'Test_Company',
        }
        serializer = CompanyModelSerializer(data=company_data)
        assert serializer.is_valid()
        company = serializer.save()
        assert isinstance(company, Company)
        assert company.name == company_data['name']


@pytest.mark.django_db
class TestBranchModelSerializer:
    @pytest.fixture
    def company(self):
        company_data = {'name': 'test_company'}
        company = Company.objects.create(**company_data)
        return company

    def test_branch_serializer_valid(self, company):
        data = {
            'name': 'test_branch',
            'address': 'London',
            'company': company,
            'phone': '394343444',
            'about': 'branch_about'
        }
        branch_serializer = BranchModelSerializer(data)
        assert branch_serializer.is_valid()
        assert branch_serializer.validated_data == data
