import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from groups.serializers import CompanyModelSerializer
from datetime import time


@pytest.fixture
def company_data():
    return {
        'name': 'Test Company',
        'logo': SimpleUploadedFile("logo.png", b"file_content", content_type="image/png"),
        'colors': 'purple',
        'start_working_time': time(hour=9, minute=00, second=00),
        'end_working_time': time(hour=18, minute=00, second=00),
        'phone': '933232323',
        'company_oferta': SimpleUploadedFile("oferta.pdf", b"file_content", content_type="application/pdf"),
    }


@pytest.mark.django_db
class TestCompanyModelSerializer:

    def test_required_fields(self):
        serializer = CompanyModelSerializer(data={})
        assert serializer.is_valid() is False
        assert set(serializer.errors.keys()) == {'name', 'phone'}

    def test_invalid_logo(self, company_data):
        company_data['logo'] = SimpleUploadedFile("logo.png", b"file_content")
        serializer = CompanyModelSerializer(data=company_data)
        assert serializer.is_valid() is False
        assert 'logo' in serializer.errors

    def test_invalid_oferta(self, company_data):
        company_data['company_oferta'] = SimpleUploadedFile("oferta.pdf", b"file_content")
        serializer = CompanyModelSerializer(data=company_data)
        assert serializer.is_valid() is False
        assert 'company_oferta' in serializer.errors

    def test_invalid_phone(self, company_data):
        company_data['phone'] = 'invalid_phone_number'
        serializer = CompanyModelSerializer(data=company_data)
        assert serializer.is_valid() is False
        assert 'phone' in serializer.errors

    def test_invalid_colors(self, company_data):
        company_data['colors'] = 'invalid_color'
        serializer = CompanyModelSerializer(data=company_data)
        assert serializer.is_valid() is False
        assert 'colors' in serializer.errors

