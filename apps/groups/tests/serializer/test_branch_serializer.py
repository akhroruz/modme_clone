import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from groups.models import Company, Branch
from groups.serializers import BranchModelSerializer


@pytest.mark.django_db
class TestBranchSerializer:
    def test_branch_model_serializer(self):
        company = Company.objects.create(name="PDP")
        branch = Branch.objects.create(
            name='ECMA',
            address='123 Main St',
            company=company,
            phone="5551234",
            about="Our main location"
        )

        serializer = BranchModelSerializer(branch)

        assert serializer.data['name'] == 'ECMA'
        assert serializer.data['address'] == '123 Main St'
        assert serializer.data['company'] == company.pk
        assert serializer.data['phone'] == '5551234'
        assert serializer.data['about'] == 'Our main location'

        image_data = SimpleUploadedFile("test_image.png", b"file_content", content_type="image/png")
        branch.image = image_data
        branch.save()
        serializer = BranchModelSerializer(branch)
        assert serializer.data['image'].startswith('/media/images/test_image')
