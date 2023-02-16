import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from groups.models import Company
from users.models import Blog, User


# TODO:Muhammad update Lead Test and create Real User

# @pytest.mark.django_db
# class TestLeadModelSerializer:
#     @pytest.fixture
#     def lead_increment(self):
#         lead_increment = LeadIncrement.objects.create(
#             name='Lead Increment 1'
#         )
#         return lead_increment
#
#     @pytest.fixture
#     def lead(self, lead_increment):
#         return Lead.objects.create(
#             full_name='full name 1',
#             comment='comment 1',
#             phone=990675624,
#             status=Lead.LeadStatus.REQUESTS,
#             lead_increment=lead_increment
#         )
#
#     def test_create_lead_model_serializer(self, lead):
#         serializer = LeadModelSerializer(lead)
#         assert serializer.data['full_name'] == lead.full_name
#         assert serializer.data['comment'] == lead.comment
#         assert serializer.data['phone'] == lead.phone
#         assert serializer.data['status'] == lead.status
#         assert serializer.data['lead_increment'] == lead.lead_increment_id
#
#     def test_delete_lead_model_serializer(self, lead):
#         lead.delete()
#         assert not Lead.objects.filter(pk=lead.pk).exists()
#
#
# @pytest.mark.django_db
# class TestLeadIncrementModelSerializer:
#     @pytest.fixture
#     def lead_increment(self):
#         lead_increment = LeadIncrement.objects.create(
#             name='Lead Increment 1'
#         )
#         return lead_increment
#
#     def test_create_lead_increment_model_serializer(self, lead_increment):
#         serializer = LeadIncrementModelSerializer(lead_increment)
#         assert serializer.data['name'] == lead_increment.name
#
#     def test_delete_lead_increment_model_serializer(self, lead_increment):
#         lead_increment.delete()
#         assert not LeadIncrement.objects.filter(pk=lead_increment.pk).exists()


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
        user = User.objects.create_user(phone='123456789', password='testpass')
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
        client.force_authenticate(user=user)
        url = reverse('news_blog-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_retrieve(self, client, user, blog, company):
        client.force_authenticate(user=user)
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client, user, company):
        client.force_authenticate(user=user)
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
        client.force_authenticate(user=user)
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
        client.force_authenticate(user=user)
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
        client.force_authenticate(user=user)
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
