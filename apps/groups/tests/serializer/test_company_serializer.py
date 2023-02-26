import pytest
from rest_framework import serializers


class CompanySerializer(serializers.Serializer):  # noqa
    name = serializers.CharField(max_length=255)


@pytest.fixture
def data():
    return {'name': 'test_company', }


def test_valid_data(data):
    serializer = CompanySerializer(data=data)
    assert serializer.is_valid()


def test_invalid_data():
    data = {'name': 'a' * 256}  # Exceeds the maximum length
    serializer = CompanySerializer(data=data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors


def test_serialization(data):
    serializer = CompanySerializer(data=data)
    assert serializer.is_valid()
    assert serializer.data == data
