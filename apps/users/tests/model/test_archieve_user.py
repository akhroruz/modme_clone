from datetime import date, time

import pytest
from django.contrib.auth.models import Group as Role
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa

from core.settings import MEDIA_ROOT
from groups.models import Company, Branch, ArchiveReason
from users.models import User, ArchivedUser


@pytest.mark.django_db
class TestArchiveUserModel:
    def test_create_archived_user(self):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        company_data = {
            'name': 'PDP',
            'logo': 'test_logo.png',
            'colors': Company.ColorChoice.RED,
            'start_working_time': time(hour=9, minute=00),
            'end_working_time': time(hour=12, minute=00),
            'phone': '991212334',
            'company_oferta': image
        }
        company = Company.objects.create(**company_data)

        branch_data = {
            'name': 'Test Branch',
            'address': 'Test Address',
            'company': company,
            'phone': '949343943',
            'about': 'Test About',
            'image': image
        }
        branch = Branch.objects.create(**branch_data)
        role_data = {'name': 'test_name'}
        role = Role.objects.create(**role_data)

        destroyer = User.objects.create(phone='998885566', password='test_1234')
        archive_reasons = ArchiveReason.objects.create(name='test_archive_reasons', company=company)

        data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'phone': '911993234',
            'birth_date': date(2000, 12, 25),
            'gender': ArchivedUser.GenderChoose.MALE,
            'photo': image,
            'balance': 12,
            'data': {"data": 'test_data'},
            'deleted_at': time(hour=8, minute=34),
            'destroyer': destroyer,
            'user_type': 'student',
            'archive_reason': archive_reasons

        }
        pre_count = ArchivedUser.objects.count()
        archieved_user = ArchivedUser.objects.create(**data)
        archieved_user.branch.add(branch)
        archieved_user.role.add(role)
        assert archieved_user.first_name == data['first_name']
        assert archieved_user.last_name == data['last_name']
        assert archieved_user.phone == data['phone']
        assert archieved_user.birth_date == data['birth_date']
        assert archieved_user.gender == data['gender']
        assert archieved_user.balance == data['balance']
        assert archieved_user.data == data['data']
        assert archieved_user.user_type == data['user_type']
        assert pre_count + 1 == ArchivedUser.objects.count()
