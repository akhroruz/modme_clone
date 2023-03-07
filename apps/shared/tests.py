import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group as Role
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.test import Client

from core.settings import MEDIA_ROOT
from groups.models import Group, Course, Room, Holiday, Branch, Company
from users.models import Lead, LeadIncrement, User, Blog


class TestBaseFixture:

    @pytest.fixture
    def user(self):
        user = get_user_model().objects.create_user(phone='901001010', password='1', is_superuser=True, is_staff=True)
        return user

    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='Company 1')
        return company

    @pytest.fixture
    def blog(self, client: Client, user, company):
        blog = Blog.objects.create(
            title='Blog 1',
            text='Text 1',
            public=True,
            created_by=user,
            updated_by=user,
            visible_all=True,
            view_count=11,
            company=company
        )
        return blog

    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(name="lead_increment1")
        return lead_increment

    @pytest.fixture
    def lead(self, lead_increment):
        lead = Lead.objects.create(
            phone=12345678,
            full_name='LeadFullname',
            comment='Lead comment',
            lead_increment=lead_increment,
            status=Lead.LeadStatus.REQUESTS
        )
        return lead

    @pytest.fixture
    def branch(self, company):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        branch = Branch.objects.create(
            name='Branch 1',
            address='Uzbekistan, Tashkent',
            phone='12345678',
            about='Something about this branch',
            company=company,
            image=image

        )
        return branch

    @pytest.fixture
    def room(self, branch):
        room = Room.objects.create(name='Room 1', branch=branch)
        return room

    @pytest.fixture
    def course(self, company):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', open(image_path, 'rb').read(), 'image/png')
        course = Course.objects.create(
            name='Course 1',
            price=2000,
            description='Course description',
            image=image,
            lesson_duration=2,
            course_duration=4,
            company=company
        )
        return course

    @pytest.fixture
    def holiday(self, branch):
        holiday = Holiday.objects.create(
            name='new year',
            holiday_date='2023-12-12',
            affect_payment=False,
            branch=branch
        )
        return holiday

    @pytest.fixture
    def group(self, branch, user, course, room):
        group = Group.objects.create(
            name='test_name',
            days=Group.DaysChoice.ODD_DAYS,
            status=Group.StatusChoice.ACTIVE,
            room=room,
            teacher=user,
            start_time='09:00:00',
            end_time='12:00:00',
            course=course,
            branch=branch,
            start_date='2023-02-23',
            end_date='2023-05-23',
            tags=['test_tag1', 'tests_tag2', 'tests_tag3'],

        )
        student1 = User.objects.create(
            phone='990675629',
            password=123,
            first_name='Mukhammad',
            last_name='Jabborov',
            is_staff=False,
            is_superuser=False
        )
        student2 = User.objects.create(
            phone='997755565',
            password=123,
            first_name='Toshpulat',
            last_name='Eshonov',
            is_staff=False,
            is_superuser=False
        )

        group.students.add(student1, student2)
        return group


@pytest.mark.django_db
class TestBase(TestBaseFixture):

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
