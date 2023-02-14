import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import Blog, Lead, LeadIncrement, User
from users.serializers import LeadModelSerializer, LeadIncrementModelSerializer


@pytest.mark.django_db
class TestLeadModelSerializer:
    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead Increment 1'
        )
        return lead_increment

    @pytest.fixture
    def lead(self, lead_increment):
        return Lead.objects.create(
            full_name='full name 1',
            comment='comment 1',
            phone=990675624,
            status=Lead.LeadStatus.REQUESTS,
            lead_increment=lead_increment
        )

    def test_create_lead_model_serializer(self, lead):
        serializer = LeadModelSerializer(lead)
        assert serializer.data['full_name'] == lead.full_name
        assert serializer.data['comment'] == lead.comment
        assert serializer.data['phone'] == lead.phone
        assert serializer.data['status'] == lead.status
        assert serializer.data['lead_increment'] == lead.lead_increment_id

    def test_delete_lead_model_serializer(self, lead):
        lead.delete()
        assert not Lead.objects.filter(pk=lead.pk).exists()


@pytest.mark.django_db
class TestLeadIncrementModelSerializer:
    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='Lead Increment 1'
        )
        return lead_increment

    def test_create_lead_increment_model_serializer(self, lead_increment):
        serializer = LeadIncrementModelSerializer(lead_increment)
        assert serializer.data['name'] == lead_increment.name

    def test_delete_lead_increment_model_serializer(self, lead_increment):
        lead_increment.delete()
        assert not LeadIncrement.objects.filter(pk=lead_increment.pk).exists()


@pytest.mark.django_db
class TestBlogModelSerializer:
    def User(self):
        return get_user_model()

    @pytest.fixture
    def client(self):
        return APIClient()

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone='123456789', password='testpass')
        return user

    @pytest.fixture
    def blog(self, user):
        blog = Blog.objects.create(
            title='Blog 1',
            text='Text 1',
            public=True,
            created_by=user,
            updated_by=user,
            visible_all=True,
            view_count=11,
        )
        return blog

    def test_list_blogs(self, client, user, blog):
        client.force_authenticate(user=user)
        url = reverse('news_blog-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_retrieve(self, client, user, blog):
        client.force_authenticate(user=user)
        url = reverse('news_blog-detail', args=(blog.id,))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == blog.title
        assert response.data['text'] == blog.text
        assert response.data['public'] == blog.public
        assert response.data['visible_all'] == blog.visible_all

    def test_create(self, client, user):
        client.force_authenticate(user=user)
        data = {
            'title': 'New Blog Title',
            'text': 'New Blog Text',
            'public': False,
            'visible_all': False,
            'view_count': 20,
        }
        url = reverse('news_blog-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update(self, client, user, blog):
        client.force_authenticate(user=user)
        data = {
            'title': 'Updated Blog Title',
            'text': 'Updated Blog Text',
            'public': True,
            'visible_all': True,
            'view_count': 30,
        }
        url = reverse('news_blog-detail', args=(blog.id,))
        response = client.put(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Blog Title'
        assert response.data['text'] == 'Updated Blog Text'
        assert response.data['public'] == True
        assert response.data['visible_all'] == True
        assert response.data['view_count'] == 30

    def test_patch(self, client, user, blog):
        client.force_authenticate(user=user)
        data = {
            'title': 'Patched Blog Title',
            'text': 'Patched Blog Text',
            'public': False,
            'visible_all': False,
            'view_count': 55
        }
        url = reverse('news_blog-detail', args=(blog.id,))
        response = client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Patched Blog Title'
        assert response.data['text'] == 'Patched Blog Text'
        assert response.data['public'] == False
        assert response.data['visible_all'] == False
        assert response.data['view_count'] == 55

    def test_delete(self, client, user, blog):
        client.force_authenticate(user=user)
        url = reverse('news_blog-detail', args=(blog.id,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
