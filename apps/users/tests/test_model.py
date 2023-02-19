import pytest

from users.models import Archive


@pytest.mark.django_db
class TestArchiveModel:
    @pytest.fixture
    def archive(self):
        archive = Archive.objects.create(name='PDP')
        return archive

    def test_archive(self, archive):
        assert archive.name == 'PDP'
        assert str(archive) == archive.name
