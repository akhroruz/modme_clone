import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group as Role
from django.contrib.contenttypes.models import ContentType

from groups.models import Group


@pytest.mark.django_db
class TestBase:

    @pytest.fixture
    def teacher_role(self):
        teacher = Role.objects.create(name='teacher')
        view_group = Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Group),
            codename='view_group'
        )
        teacher.permissions.add(*view_group)
        return teacher

    @pytest.fixture
    def user(self):
        user = get_user_model().objects.create_user(
            phone='901001010',
            password='1'
        )
        return user

    @pytest.fixture
    def teacher(self, user, teacher_role):
        user.role.add(teacher_role)
        return user
