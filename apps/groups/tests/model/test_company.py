import pytest  # noqa

from groups.models import Company


@pytest.mark.django_db
class TestCompanyModel:
    def test_create_company(self):  # noqa
        data = {'name': 'PDP'}
        company_count = Company.objects.count()
        company = Company.objects.create(**data)
        assert company.name == data['name']
        assert str(company) == company.name
        assert company_count + 1 == Company.objects.count()
