from io import BytesIO

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.groups.models import Role
from apps.groups.serializers import RoleModelSerializer
from apps.groups.models import Branch
from apps.groups.serializers import BranchModelSerializer


@pytest.mark.django_db
class TestRoleModelSerializer:

    @pytest.fixture
    def role(self):
        return Role.objects.create(name='Role 1')

    def test_role_model_serializer(self, role):
        serializer = RoleModelSerializer(role)
        assert serializer.data['name'] == role.name


def temporary_image():
    bts = BytesIO()
    img = Image.new("RGB", (100, 100))
    img.save(bts, 'png')
    return SimpleUploadedFile("media/images/test.png", bts.getvalue())


@pytest.mark.django_db
class TestBranchModelSerializer:
    @pytest.fixture
    def branch(self):
        return Branch.objects.create(
            name='Branch 1',
            address='Address 1',
            phone_number=990675624,
            about='Text 1',
            image='media/images/' + temporary_image().name
        )

    def test_branch_model_serializer(self, branch):
        serializer = BranchModelSerializer(branch)
        assert serializer.data['name'] == branch.name
        assert serializer.data['address'] == branch.address
        assert serializer.data['phone_number'] == branch.phone_number
        assert serializer.data['about'] == branch.about
        assert serializer.data['image'] == branch.image
