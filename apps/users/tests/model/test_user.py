from datetime import date
import pytest
from django.contrib.auth.models import Group as Role
from groups.models import Company, Branch
from users.models import Archive, User


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        company_data = {'name': 'test_company'}
        company = Company.objects.create(**company_data)

        branch_data = {
            'name': 'test_name',
            'address': 'test_address',
            'company': company,
            'phone': '933432343',
            'about': 'test_about',
            'image': 'test_image.png',
        }
        branch = Branch.objects.create(**branch_data)

        archive_data = {'name': 'PDP'}
        archive = Archive.objects.create(**archive_data)

        role_data = {'name': 'test_name'}
        role = Role.objects.create(**role_data)

        data = {
            'phone': '3232923',
            'is_archive': True,
            'archive': archive,
            'birth_date': date(2002, 12, 25),
            'gender': 'Male',
            'photo': 'test_photo.png',
            'balance': 550,
            'data': {'social_account': 'twitter', 'password': '1'},
            'deleted_at': date(2022, 12, 25),
        }
        user_count = User.objects.count()
        user = User.objects.create(**data)
        user.branch.add(branch)
        user.role.add(role)

        assert user.phone == data['phone']
        assert user.is_archive
        assert user.birth_date == data['birth_date']
        assert user.gender == data['gender']
        assert user.photo == data['photo']
        assert user.balance == data['balance']
        assert user.data == data['data']
        assert user.deleted_at == data['deleted_at']
        assert user_count + 1 == User.objects.count()
