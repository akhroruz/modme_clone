import pytest
from django.contrib.contenttypes.models import ContentType

from groups.models import Company
from users.models import LeadIncrement, Lead, Blog, User, Comment


@pytest.mark.django_db
class TestLeadModel:
    def test_lead(self):
        lead_increment = LeadIncrement.objects.create(
            name='test_name'
        )

        lead = Lead.objects.create(
            full_name='test_fullname',
            comment='test_comment',
            phone=934492123,
            status='Requests',
            lead_increment=lead_increment
        )

        assert lead.full_name == 'test_fullname'
        assert lead.comment == 'test_comment'
        assert lead.phone == 934492123
        assert lead.status == 'Requests'
        assert lead.lead_increment == lead_increment
        assert str(lead) == f'{lead.full_name} | {lead.phone}'


@pytest.mark.django_db
class TestBlogModel:
    @pytest.fixture
    def company(self):
        company = Company.objects.create(
            name='test_company'
        )
        return company

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone=1234567, password='pass')
        return user

    @pytest.fixture
    def blog(self, company, user):
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
