import pytest
from users.models import Archive


@pytest.mark.django_db
class TestArchiveModel:

    def test_create_archive(self):  # noqa
        data = {'name': 'PDP'}
        count = Archive.objects.count()
        archive = Archive.objects.create(**data)
        assert archive.name == data['name']
        assert str(archive) == archive.name
        assert count + 1 == Archive.objects.count()
