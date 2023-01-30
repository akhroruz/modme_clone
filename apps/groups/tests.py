import pytest

from groups.models import Role


@pytest.mark.django_db
class TestRoleModel:

    @pytest.fixture
    def role(self):
        role = Role.objects.create(name='Role 1')
        return role

    def test_role_create_model(self):  # model
        name = 'Role 2'
        count = Role.objects.count()
        role = Role.objects.create(name=name)
        assert role.name == name
        assert Role.objects.count() - 1 == count