import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group as Role
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from groups.models import Group, Course, Room, Holiday, Branch
from users.models import Lead, LeadIncrement, Archive


@pytest.mark.django_db
class TestBase:

    @pytest.fixture
    def ceo_role(self):
        ceo = Role.objects.create(name='ceo')
        permissions = Permission.objects.all()
        ceo.permissions.add(*permissions)
        return ceo

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
    def administrator_role(self):
        administrator = Role.objects.create(name='administrator')
        branch_director = Role.objects.create(name='branch_director')
        permissions = Permission.objects.filter(
            Q(
                Q(codename='view_course') | Q(codename='change_course') | Q(codename='delete_course') | Q(
                    codename='add_course'),
                content_type=ContentType.objects.get_for_model(Course)
            ) |
            Q(
                Q(codename='view_group') | Q(codename='change_group') | Q(codename='delete_group') | Q(
                    codename='add_group'),
                content_type=ContentType.objects.get_for_model(Group)
            ) |
            Q(
                Q(codename='view_room') | Q(codename='change_room') | Q(codename='delete_room') | Q(
                    codename='add_room'),
                content_type=ContentType.objects.get_for_model(Room)
            ) |
            Q(
                Q(codename='view_lead') | Q(codename='change_lead') | Q(codename='delete_lead') | Q(
                    codename='add_lead'),
                content_type=ContentType.objects.get_for_model(Lead)
            ) |
            Q(
                Q(codename='view_leadincrement') | Q(codename='change_leadincrement') | Q(
                    codename='delete_leadincrement') | Q(
                    codename='add_leadincrement'),
                content_type=ContentType.objects.get_for_model(LeadIncrement)
            ) |
            Q(
                Q(codename='view_holiday') | Q(codename='change_holiday') | Q(
                    codename='delete_holiday') | Q(
                    codename='add_holiday'),
                content_type=ContentType.objects.get_for_model(Holiday)
            ) |
            Q(
                Q(codename='view_archive') | Q(codename='change_archive') | Q(
                    codename='delete_archive') | Q(
                    codename='add_archive'),
                content_type=ContentType.objects.get_for_model(Archive)
            ) |
            Q(
                Q(codename='view_branch'), content_type=ContentType.objects.get_for_model(Branch)
            ) |
            Q(
                Q(codename='view_user') | Q(codename='change_user'),
                content_type=ContentType.objects.get_for_model(Branch)
            )

        )
        administrator.permissions.add(*permissions)
        branch_director.permissions.add(*permissions)
        return administrator

    # @pytest.fixture
    # def limit_admin_role(self):
    #     limit_admin = Role.objects.create(name='limited_administrator')
    #     permissions = Permission.objects.filter(
    #         Q(
    #             Q(codename='view_course') | Q(codename='change_course') | Q(codename='delete_course') | Q(
    #                 codename='add_course'),
    #             content_type=ContentType.objects.get_for_model(Course)
    #         ) |
    #         Q(
    #             Q(codename='view_group') | Q(codename='change_group') | Q(codename='delete_group') | Q(
    #                 codename='add_group'),
    #             content_type=ContentType.objects.get_for_model(Group)
    #         ) |
    #         Q(
    #             Q(codename='view_room') | Q(codename='change_room') | Q(codename='delete_room') | Q(
    #                 codename='add_room'),
    #             content_type=ContentType.objects.get_for_model(Room)
    #         ) |
    #         Q(
    #             Q(codename='view_lead') | Q(codename='change_lead') | Q(codename='delete_lead') | Q(
    #                 codename='add_lead'),
    #             content_type=ContentType.objects.get_for_model(Lead)
    #         ) |
    #         Q(
    #             Q(codename='view_leadincrement') | Q(codename='change_leadincrement') | Q(
    #                 codename='delete_leadincrement') | Q(
    #                 codename='add_leadincrement'),
    #             content_type=ContentType.objects.get_for_model(LeadIncrement)
    #         ) |
    #         Q(
    #             Q(codename='view_holiday') | Q(codename='change_holiday') | Q(
    #                 codename='delete_holiday') | Q(
    #                 codename='add_holiday'),
    #             content_type=ContentType.objects.get_for_model(Holiday)
    #         ) |
    #         Q(
    #             Q(codename='view_archive') | Q(codename='change_archive') | Q(
    #                 codename='delete_archive') | Q(
    #                 codename='add_archive'),
    #             content_type=ContentType.objects.get_for_model(Archive)
    #         ) |
    #         Q(
    #             Q(codename='view_branch'), content_type=ContentType.objects.get_for_model(Branch)
    #         ) |
    #         Q(
    #             Q(codename='view_user') | Q(codename='change_user'),
    #             content_type=ContentType.objects.get_for_model(Branch)
    #         )
    #
    #     )
    #     administrator.permissions.add(*permissions)
    #     branch_director.permissions.add(*permissions)
    #     return administrator

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

    @pytest.fixture
    def administrator(self, user, administrator_role):
        user.role.add(administrator_role)
        return user

    @pytest.fixture
    def branch_director(self, user, administrator_role):
        user.role.add(administrator_role)
        return user
