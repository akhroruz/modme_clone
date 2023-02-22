import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group as Role
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from groups.models import Group, Course, Room, Holiday, Branch
from users.models import Lead, LeadIncrement, User, Archive


@pytest.mark.django_db
class TestBase:

    # def set_permissions(self, role_name: str, perms: list = None, model=None):
    #     role = Role.objects.create(name=role_name)
    #
    #     if model != None:
    #         content_type = ContentType.objects.get_for_model(model)
    #         permissions = Permission.objects.filter(content_type=content_type)
    #         model_name = model.__name__.lower()
    #         for permission in permissions:
    #             codename = permission.codename
    #             if codename.startswith('view_') and 'view' in perms:
    #                 permission_name = 'view_' + model_name
    #             elif codename.startswith('change_') and 'change' in perms:
    #                 permission_name = 'change_' + model_name
    #             elif codename.startswith('delete_') and 'delete' in perms:
    #                 permission_name = 'delete_' + model_name
    #             elif codename.startswith('add_') and 'add' in perms:
    #                 permission_name = 'add_' + model_name
    #             else:
    #                 continue
    #
    #             permission_name = 'auth.' + permission_name
    #             permission = Permission.objects.get(codename=permission_name)
    #             role.permissions.add(permission)
    #     else:
    #         permission = Permission.objects.all()
    #         role.permissions.add(*permission)
    #     return role

    @pytest.fixture
    def user(self):
        user = get_user_model().objects.create_user(
            phone='901001010',
            password='1'
        )
        return user

    @pytest.fixture
    def ceo(self, user):
        ceo = Role.objects.create(name='ceo')
        permissions = Permission.objects.all()
        ceo.permissions.add(*permissions)
        user.role.add(ceo)
        return user

    @pytest.fixture
    def teacher(self, user):
        teacher = Role.objects.create(name='teacher')
        view_group = Permission.objects.filter(
            codename='view_group', content_type=ContentType.objects.get_for_model(Group)
        )
        teacher.permissions.add(*view_group)
        user.role.add(teacher)
        return user

    @pytest.fixture
    def administrator(self, user):
        administrator = Role.objects.create(name='administrator')
        branch_director = Role.objects.create(name='branch_director')
        permissions = Permission.objects.filter(
            Q(
                codename__in=('view_course', 'change_course', 'delete_course', 'add_course'),
                content_type=ContentType.objects.get_for_model(Course)
            ) |
            Q(
                codename__in=('view_group', 'change_group', 'delete_group', 'add_group'),
                content_type=ContentType.objects.get_for_model(Group)
            ) |
            Q(
                codename__in=('view_archive', 'change_archive', 'delete_archive', 'add_archive'),
                content_type=ContentType.objects.get_for_model(Archive)
            ) |
            Q(
                codename__in=('view_room', 'change_room', 'delete_room', 'add_room'),
                content_type=ContentType.objects.get_for_model(Room)
            ) |
            Q(
                codename__in=('view_lead', 'change_lead', 'delete_lead', 'add_lead'),
                content_type=ContentType.objects.get_for_model(Lead)
            ) |
            Q(
                codename__in=('view_leadincrement', 'change_leadincrement', 'delete_leadincrement',
                              'add_leadincrement'),
                content_type=ContentType.objects.get_for_model(LeadIncrement)
            ) |
            Q(
                codename__in=('view_holiday', 'change_holiday', 'delete_holiday', 'add_holiday'),
                content_type=ContentType.objects.get_for_model(Holiday)
            ) |
            Q(
                codename='view_branch',
                content_type=ContentType.objects.get_for_model(Branch)
            ) |
            Q(
                codename__in=('view_user', 'change_user'),
                content_type=ContentType.objects.get_for_model(User)
            )
        )
        administrator.permissions.add(*permissions)
        branch_director.permissions.add(*permissions)
        user.role.add(administrator)
        return user

    @pytest.fixture
    def marketer(self, user):
        marketer = Role.objects.create(name='marketer')
        permissions = Permission.objects.filter(
            Q(
                codename__in=('view_lead', 'change_lead', 'delete_lead', 'add_lead'),
                content_type=ContentType.objects.get_for_model(Lead)
            ) |
            Q(
                codename__in=('view_leadincrement', 'change_leadincrement', 'delete_leadincrement',
                              'add_leadincrement'),
                content_type=ContentType.objects.get_for_model(LeadIncrement)
            )
        )
        marketer.permissions.add(*permissions)
        user.role.add(marketer)
        return user

    @pytest.fixture
    def limit_admin(self, user):
        limit_admin = Role.objects.create(name='limited_administrator')
        permissions = Permission.objects.filter(
            Q(
                codename__in=('view_course', 'change_course', 'delete_course', 'add_course'),
                content_type=ContentType.objects.get_for_model(Course)
            ) |
            Q(
                codename__in=('view_group', 'change_group', 'delete_group', 'add_group'),
                content_type=ContentType.objects.get_for_model(Group)
            ) |
            Q(
                codename='view_branch', content_type=ContentType.objects.get_for_model(Branch)
            ) |
            Q(
                codename__in=('view_user', 'change_user'),
                content_type=ContentType.objects.get_for_model(User)
            )
        )
        limit_admin.permissions.add(*permissions)
        user.role.add(limit_admin)
        return user

    @pytest.fixture
    def cashier(self, user):
        cashier = Role.objects.create(name='cashier')
        permissions = Permission.objects.filter(
            Q(
                codename__in=('view_user', 'change_user'),
                content_type=ContentType.objects.get_for_model(User)
            )
        )
        cashier.permissions.add(*permissions)
        user.role.add(cashier)
        return cashier
