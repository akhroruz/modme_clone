from datetime import date
import pytest
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group as Role
from groups.models import Company, Branch
from users.models import Archive, LeadIncrement, Lead, User, Blog, Comment


@pytest.mark.django_db
class TestArchiveModel:

    def test_archive(self):
        data = {'name': 'PDP'}
        count = Archive.objects.count()
        archive = Archive.objects.create(**data)
        assert archive.name == data['name']
        assert str(archive) == archive.name
        assert count + 1 == Archive.objects.count()


@pytest.mark.django_db
class TestLeadIncrementModel:
    def test_lead_increment(self):
        data = {'name': 'test_name'}
        lead_increment = LeadIncrement.objects.create(**data)
        assert lead_increment.name == data['name']
        assert str(lead_increment) == lead_increment.name


@pytest.mark.django_db
class TestLeadModel:
    def test_lead(self):
        lead_increment = LeadIncrement.objects.create(
            name='test_name'
        )
        data = {
            'full_name': 'test_fullname',
            'comment': 'test_comment',
            'phone': 934492123,
            'status': 'Requests',
            'lead_increment': lead_increment
        }
        count = Lead.objects.count()
        lead = Lead.objects.create(**data)
        assert lead.full_name == data['full_name']
        assert lead.comment == data['comment']
        assert lead.phone == data['phone']
        assert lead.status == data['status']
        assert lead.lead_increment == data['lead_increment']
        assert str(lead) == f'{lead.full_name} | {lead.phone}'
        assert count + 1 == Lead.objects.count()


@pytest.mark.django_db
class TestBlogModel:

    def test_create_blog(self):
        company = Company.objects.create(
            name='test_company'
        )
        user = User.objects.create_user(phone=1234567, password='pass')
        blog = Blog.objects.create(
            title='test_title',
            text='test_text',
            public=True,
            created_by=user,
            updated_by=user,
            visible_all=True,
            view_count=100,
            company=company
        )
        assert blog.title == 'test_title'
        assert blog.text == 'test_text'
        assert blog.public
        assert blog.created_by == user
        assert blog.updated_by == user
        assert blog.visible_all
        assert blog.view_count == 100
        assert blog.company == company
        assert str(blog) == blog.title


@pytest.mark.django_db
class TestCommentModel:
    # TODO Javlon
    @pytest.fixture
    def comment(self):
        content_type = ContentType.objects.get_for_model(User)
        comment = Comment.objects.create(
            text='test_text',
            content_type=content_type,
            object_id=1,
        )

        assert comment.text == 'test_text'
        assert comment.object_id == 1


@pytest.mark.django_db
class TestUserModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(name='test_name')
        return company

    @pytest.fixture
    def branch(self, company):
        branch = Branch.objects.create(
            name='test_name',
            address='test_address',
            company=company,
            phone=934342334,
            about='test_about',
            image='test_image.png'
        )
        return branch

    @pytest.fixture
    def archive(self):
        archive = Archive.objects.create(name='test_name')
        return archive

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(
            phone='1233434',
            password='test_password',
        )
        return user

    @pytest.fixture
    def role(self):
        role = Role.objects.create(name='test_name')
        return role

    @pytest.fixture
    def user(self, archive, role, branch):
        user = User.objects.create(
            phone='3232923',
            is_archive=True,
            archive=archive,
            birth_date=date(2002, 12, 25),
            gender='Male',
            photo='test_photo.png',
            balance=550,
            data={'social_account': 'twitter', 'password': '1'},
            deleted_at=date(2022, 12, 25),
        )
        user.branch.add(branch)
        user.role.add(role)

        assert user.phone == '3232923'
        assert user.is_archive
        assert user.birth_date == date(2002, 12, 25)
        assert user.gender == 'Male'
        assert user.photo == 'test_photo.png'
        assert user.balance == 550
        assert user.data == {'social_account': 'twitter', 'password': '1'}
        assert user.deleted_at == date(2022, 12, 25)
