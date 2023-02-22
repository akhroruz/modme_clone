from datetime import date
import pytest
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group as Role
from groups.models import Company, Branch
from users.models import Archive, LeadIncrement, Lead, User, Blog, Comment


@pytest.mark.django_db
class TestArchiveModel:

    def test_archive(self):
        archive_data = {
            'name': 'PDP'
        }
        count = Archive.objects.count()
        archive = Archive.objects.create(**archive_data)
        assert archive.name == archive_data['name']
        assert str(archive) == archive.name
        assert count + 1 == Archive.objects.count()


@pytest.mark.django_db
class TestLeadIncrementModel:
    def test_lead_increment(self):
        lead_data = {
            'name': 'test_name'
        }
        lead_increment = LeadIncrement.objects.create(**lead_data)
        assert lead_increment.name == lead_data['name']
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
        company_data = {
            'name': 'test_company'
        }
        company = Company.objects.create(**company_data)
        user_data = {
            'phone': 1234567,
            'password': 'pass'
        }
        user = User.objects.create_user(**user_data)

        blog_data = {
            'title': 'test_title',
            'text': 'test_text',
            'public': True,
            'created_by': user,
            'updated_by': user,
            'visible_all': True,
            'view_count': 100,
            'company': company
        }
        blog_count = Blog.objects.count()
        blog = Blog.objects.create(**blog_data)
        assert blog.title == blog_data['title']
        assert blog.text == blog_data['text']
        assert blog.public
        assert blog.created_by == user
        assert blog.updated_by == user
        assert blog.visible_all
        assert blog.view_count == 100
        assert blog.company == company
        assert str(blog) == blog.title
        assert blog_count + 1 == Blog.objects.count()


@pytest.mark.django_db
class TestCommentModel:
    def test_create_comment(self):
        content_type = ContentType.objects.get_for_model(User)
        comment_data = {
            'text': 'test_text',
            'content_type': content_type,
            'object_id': 1
        }
        comment_count = Comment.objects.count()
        comment = Comment.objects.create(**comment_data)
        assert comment.text == comment_data['text']
        assert comment.object_id == comment_data['object_id']
        assert comment_count + 1 == Comment.objects.count()


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        company_data = {
            'name': 'test_company'
        }
        company = Company.objects.create(**company_data)

        branch_data = {
            'name': 'test_name',
            'address': 'test_address',
            'company': company,
            'phone': '933432343',
            'about': 'test_about',
            'image': 'test_image.png',
        }
        branch = Branch.objects.create(**branch_data)

        archive_data = {
            'name': 'PDP'
        }
        archive = Archive.objects.create(**archive_data)

        role_data = {
            'name': 'test_name'
        }
        role = Role.objects.create(**role_data)

        user_data = {
            'phone': '3232923',
            'is_archive': True,
            'archive': archive,
            'birth_date': date(2002, 12, 25),
            'gender': 'Male',
            'photo': 'test_photo.png',
            'balance': 550,
            'data': {'social_account': 'twitter', 'password': '1'},
            'deleted_at': date(2022, 12, 25),
        }
        user_count = User.objects.count()
        user = User.objects.create(**user_data)
        user.branch.add(branch)
        user.role.add(role)

        assert user.phone == user_data['phone']
        assert user.is_archive
        assert user.birth_date == user_data['birth_date']
        assert user.gender == user_data['gender']
        assert user.photo == user_data['photo']
        assert user.balance == user_data['balance']
        assert user.data == user_data['data']
        assert user.deleted_at == user_data['deleted_at']
        assert user_count + 1 == User.objects.count()
