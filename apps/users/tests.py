import pytest

from apps.users.models import User


@pytest.mark.django_db
class TestUserAPIView:
    @pytest.fixture
    def users(self, db, client):
        user = User.objects.create(name='User 1')
        return user
