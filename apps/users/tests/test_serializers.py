import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from groups.models import Company
from users.models import Blog, User, Lead, LeadIncrement


@pytest.mark.django_db
class TestLeadModelSerializer:

    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead Increment 1'
        )
        return lead_increment

    def test_lead_increment_list(self, client, lead_increment):
        client.force_login(lead_increment)
        url = reverse('lead_increment-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_create_lead_increment(self, client, lead_increment):
        client.force_login(user=lead_increment)
        data = {
            'name': 'New Lead Increment',

        }
        url = reverse('lead_increment-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New Lead Increment'

    def test_update_lead_increment(self, client, lead_increment):
        client.force_login(user=lead_increment)
        data = {
            'name': 'Updated Lead Increment'
        }

        url = reverse('lead_increment-detail', args=(lead_increment.id,))
        response = client.put(url, data)
        assert response.status_code == 200
        assert response.data['name'] == 'Updated Lead Increment'

    def test_patch_lead_increment(self, client, lead_increment):
        client.force_login(user=lead_increment)
        data = {
            'name': 'Patched Lead Increment'
        }

        url = reverse('lead_increment-detail', args=(lead_increment.id,))
        response = client.put(url, data)
        assert response.status_code == 200
        assert response.data['name'] == 'Patched Lead Increment'

    def test_delete(self, client, lead_increment):
        client.force_login(user=lead_increment)
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestBlogModelSerializer:

    @pytest.fixture
    def company(self):
        company = Company.objects.create(
            name='Company 1',
        )
        return company

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone=1234567, password='pass')
        return user

    @pytest.fixture
    def blog(self, user, client, company):
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

    def test_list_blogs(self, client, user, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_retrieve(self, client, user, rf, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client, user, company):
        client.force_login(user)
        data = {
            'title': 'New Blog Title',
            'text': 'New Blog Text',
            'public': False,
            'visible_all': False,
            'view_count': 20,
            'company': company.pk
        }
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update(self, client, user, blog, company):
        client.force_login(user)
        data = {
            'title': 'Updated Blog Title',
            'text': 'Updated Blog Text',
            'public': True,
            'visible_all': True,
            'view_count': 30,
            'company': company.pk

        }
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Blog Title'
        assert response.data['text'] == 'Updated Blog Text'
        assert response.data['public']
        assert response.data['visible_all']
        assert response.data['view_count'] == 30

    def test_patch(self, client, user, blog, company):
        client.force_login(user)
        data = {
            'title': 'Patched Blog Title',
            'text': 'Patched Blog Text',
            'public': False,
            'visible_all': False,
            'view_count': 55,

        }
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Patched Blog Title'
        assert response.data['text'] == 'Patched Blog Text'
        assert not response.data['public']
        assert not response.data['visible_all']
        assert response.data['view_count'] == 55

    def test_delete(self, client, user, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class LeadModelSerializerTest:
    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead Increment 1'
        )
        return lead_increment

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def lead(self, lead_increment):
        lead = Lead.objects.create(
            full_name='LeadFullName1',
            comment='Comment1',
            phone='123456789',
            status=Lead.LeadStatus.REQUESTS,
            lead_increment_id=lead_increment.pk
        )
        return lead

    def test_lead_list(self, client, lead):
        client.force_login(user=lead)
        url = reverse('lead-list')
        response = client.get(url)
        assert response.status_code == 200

    def test_create_lead(self, client, lead, lead_increment):
        client.force_login(user=lead)
        data = {
            'full_name': 'New Created Lead',
            'comment': 'New Created Comment',
            'phone': '7777777',
            'status': Lead.LeadStatus.PENDING,
            'lead_increment': lead_increment.pk
        }
        url = reverse('lead-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['full_name'] == 'New Created Lead'
        assert response.data['comment'] == 'New Created Comment'
        assert response.data['phone'] == 7777777
        assert response.data['status'] == lead.LeadStatus.PENDING
        assert response.data['lead_increment'] == lead_increment.pk

# TODO: Adkhamjon
# @pytest.mark.django_db
# class TestUserModelSerializer:
#
#     @pytest.fixture
#     def client(self):
#         return APIClient()
#
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(
#             name='Company1 PDP',
#         )
#         return company
#
#     @pytest.fixture
#     def branch(self, company):
#         image_path = MEDIA_ROOT + '/test.png'
#         image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
#         branch = Branch.objects.create(
#             name='branch1',
#             address='address1',
#             company_id=company.pk,
#             phone='1234567',
#             image=image
#         )
#         return branch
#
#     @pytest.fixture
#     def role(self):
#         role = 'CEO'
#         return role
#
#     @pytest.fixture
#     def archive(self):
#         archive = Archive.objects.create(
#             name='ARCHIVE SITY'
#         )
#         return archive
#
#     @pytest.fixture
#     def user(self, archive, role, branch):
#         image_path = MEDIA_ROOT + '/test.png'
#         image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
#         user = User.objects.create_user(
#             phone=12345678,
#             is_archive=False,
#             archive_id=archive.pk,
#             birth_date='2004-10-10',
#             photo=image,
#             balance=2,
#             # role=role,
#             # branch=branch.pk,
#             data='JSON DATA',
#         )
#         return user
#
#     #
#     # def test_user_list(self, client, user, branch, company, archive, role):
#     #     client.force_login(user)
#     #     url = reverse('news_blog-list'),
#     #     response = client.get(url)
#     #     assert response.status_code == 200
#     #     assert len(response.data) == 1
#
#     def test_create(self, client, user, archive):
#         image_path = MEDIA_ROOT + '/test.png'
#         image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
#         client.force_login(user)
#         data = {
#             'phone': '77777777',
#             'is_archive': True,
#             'archive_id': archive.pk,
#             'birth_date': '2000-01-01',
#             'photo': image,
#             'balance': 45,
#             'gender': user.GenderChoose.MALE,
#             # 'role': role,
#             # 'branch': branch.pk,
#             'data': 'DATA NEW CREATED'
#         }
#
#         url = reverse('user-list')
#         response = client.post(url, data)
#         assert response.status_code == 201
#         assert response.data['phone'] == 77777777
#         assert response.data['gender'] == user.GenderChoose.MALE
#         assert response.data['is_active']
#         assert response.data['archive_id'] == archive.pk
#         assert response.data['birth_data'] == '2000-01-01'
#         assert response.data['balance'] == 45
#         # assert response.data['role'] == role.id
#         # assert response.data['branch'] == branch.pk
#         assert response.data['data'] == 'DATA NEW CREATED'
