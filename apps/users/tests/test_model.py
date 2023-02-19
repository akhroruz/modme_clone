# import pytest
#
# from groups.models import Company
# from users.models import Archive, LeadIncrement, Lead, Blog, User
#
#
# @pytest.mark.django_db
# class TestArchiveModel:
#     @pytest.fixture
#     def archive(self):
#         archive = Archive.objects.create(name='PDP')
#         return archive
#
#     def test_archive(self, archive):
#         assert archive.name == 'PDP'
#         assert str(archive) == archive.name
#
#
# @pytest.mark.django_db
# class TestLeadIncrementModel:
#     @pytest.fixture
#     def lead_increment(self):
#         lead_increment = LeadIncrement.objects.create(
#             name='test_name'
#         )
#         return lead_increment
#
#     def test_lead_increment(self, lead_increment):
#         assert lead_increment.name == 'test_name'
#         assert str(lead_increment) == lead_increment.name
#
#
# @pytest.mark.django_db
# class TestLeadModel:
#     @pytest.fixture
#     def lead_increment(self):
#         lead_increment = LeadIncrement.objects.create(
#             name='test_name'
#         )
#         return lead_increment
#
#     @pytest.fixture
#     def lead(self, lead_increment):
#         lead = Lead.objects.create(
#             full_name='test_fullname',
#             comment='test_comment',
#             phone=934492123,
#             status='Requests',
#             lead_increment=lead_increment
#         )
#         return lead
#
#     def test_lead(self, lead, lead_increment):
#         assert lead.full_name == 'test_fullname'
#         assert lead.comment == 'test_comment'
#         assert lead.phone == 934492123
#         assert lead.status == 'Requests'
#         assert lead.lead_increment == lead_increment
#         assert str(lead) == f'{lead.full_name} | {lead.phone}'
#
#
# @pytest.mark.django_db
# class TestBlogModel:
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(
#             name='test_company'
#         )
#         return company
#
#     @pytest.fixture
#     def user(self):
#         user = User.objects.create_user(phone=1234567, password='pass')
#         return user
#
#     @pytest.fixture
#     def blog(self, company, user):
#         blog = Blog.objects.create(
#             title='test_title',
#             text='test_text',
#             public=True,
#             created_by=user,
#             updated_by=user,
#             visible_all=True,
#             view_count=100,
#             company=company
#         )
#         return blog
#
#     def test_blog(self, blog, company, user):
#         assert blog.title == 'test_title'
#         assert blog.text == 'test_text'
#         assert blog.public == True
#         assert blog.created_by == user
#         assert blog.updated_by == user
#         assert blog.visible_all == True
#         assert blog.view_count == 100
#         assert blog.company == company
#         assert str(blog) == blog.title
