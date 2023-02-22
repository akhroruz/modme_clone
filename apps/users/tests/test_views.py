import pytest
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework import status
from rest_framework.reverse import reverse
from groups.models import Company
from users.models import User, Archive, Blog, LeadIncrement, Lead


@pytest.mark.django_db
class TestBlogModelViewSet:

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone=1234567, password='password')
        return user

    @pytest.fixture
    def company(self):
        company = Company.objects.create(
            name='Company 1',
        )
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

    def test_list_blogs(self, client: Client, user, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.get(url)
        assert Blog.objects.count() == response.data['count']
        assert response.status_code == status.HTTP_200_OK

    def test_create_blog(self, client: Client, user, company):
        client.force_login(user)
        data = {
            'title': 'Title1',
            'text': 'Text1',
            'public': False,
            'visible_all': False,
            'view_count': 20,
            'company': company.pk,
        }
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        count = Blog.objects.count()
        response = client.post(url, data)
        keys = {'title', 'text', 'public', 'visible_all', 'view_count', 'company'}
        assert len(keys.difference(set(response.json()))) == 0
        assert data == response.json()
        assert Blog.objects.count() - 1 == count
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_blog(self, client: Client, user, blog, company):
        client.force_login(user)
        data = {
            'title': 'updated_blog',
            'text': 'updated_texy',
            'public': True,
            'visible_all': True,
            'view_count': 30,
            'company': company.pk
        }

        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.put(url, data, 'application/json')
        keys = {'title', 'text', 'public', 'visible_all', 'view_count', 'company'}
        assert len(keys.difference(set(response.json()))) == 0
        assert data == response.json()
        assert response.status_code == status.HTTP_200_OK

    def test_patch_blog(self, client: Client, user, blog, company):
        client.force_login(user)
        data = {
            'title': 'patched_title',
            'text': 'patched_text',
            'public': False,
            'visible_all': False,
            'view_count': 55,
            'company': company.pk
        }

        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.patch(url, data, 'application/json')
        keys = {'title', 'text', 'public', 'visible_all', 'view_count', 'company'}
        assert len(keys.difference(set(response.json()))) == 0
        assert data == response.json()
        assert response.status_code == status.HTTP_200_OK

    def test_delete_blog(self, client: Client, user, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        count = Blog.objects.count()
        response = client.delete(url)
        assert Blog.objects.count() + 1 == count
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestLeadIncrementModelViewSet:
    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone=1234567, password='pass')
        return user

    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name="lead_increment1"
        )
        return lead_increment

    def test_lead_increment_list(self, client: Client, user):
        client.force_login(user)
        url = reverse('lead_increment-list')
        response = client.get(url)
        assert LeadIncrement.objects.count() == response.data['count']
        assert response.status_code == status.HTTP_200_OK

    def test_create_lead_increment(self, client: Client, user):
        client.force_login(user)
        data = {'name': 'new_increment'}
        url = reverse('lead_increment-list')
        count = LeadIncrement.objects.count()
        response = client.post(url, data)
        assert response.data['name'] == data['name']
        assert LeadIncrement.objects.count() - 1 == count
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_lead_increment(self, client: Client, user, lead_increment):
        client.force_login(user)
        data = {'name': 'created_new_increment'}
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        response = client.put(url, data, 'application/json')
        assert response.data['name'] == data['name']
        assert response.status_code == status.HTTP_200_OK

    def test_patch_lead_increment(self, client: Client, user, lead_increment):
        client.force_login(user)
        data = {'name': 'patched_Increment'}
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        response = client.patch(url, data, 'application/json')
        assert response.data['name'] == data['name']
        assert response.status_code == status.HTTP_200_OK

    def test_delete_lead_increment(self, client: Client, user, lead_increment):
        client.force_login(user)
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        count = LeadIncrement.objects.count()
        response = client.delete(url)
        assert LeadIncrement.objects.count() + 1 == count
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestLeadModelViewSet:

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone=1234567, password='pass')
        return user

    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name="lead_increment1"
        )
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

    def test_lead_list(self, client: Client, user, lead):
        client.force_login(user)
        url = reverse('lead-list')
        response = client.get(url)
        assert Lead.objects.count() == response.data['count']
        assert response.status_code == status.HTTP_200_OK

    def test_create_lead(self, client: Client, user, lead_increment):
        client.force_login(user)
        data = {
            'phone': 66666666,
            'full_name': 'New Lead',
            'comment': 'comment1',
            'lead_increment': lead_increment.pk,
            'status': Lead.LeadStatus.COLLECT
        }
        url = reverse('lead-list')
        count = Lead.objects.count()
        response = client.post(url, data)
        keys = {'phone', 'full_name', 'comment', 'lead_increment', 'status'}
        assert Lead.objects.count() - 1 == count
        assert len(keys.difference(set(response.json()))) == 0
        assert data == response.json()
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_lead(self, client: Client, user, lead, lead_increment):
        client.force_login(user)
        data = {
            'phone': 1111111,
            'full_name': 'Updated_full_name',
            'comment': 'Updated_comment',
            'lead_increment': lead_increment.pk,
            'status': Lead.LeadStatus.COLLECT
        }
        url = reverse('lead-detail', args=(lead.pk,))
        response = client.put(url, data, 'application/json')
        keys = {'phone', 'full_name', 'comment', 'lead_increment', 'status'}
        assert len(keys.difference(set(response.json()))) == 0
        assert data == response.json()
        assert response.status_code == status.HTTP_200_OK

    def test_patch_lead(self, client: Client, lead, user, lead_increment):
        client.force_login(user)
        data = {
            'phone': 555555,
            'full_name': 'patched_full_name',
            'comment': 'patched_comment',
            'lead_increment': lead_increment.pk,
            'status': Lead.LeadStatus.PENDING
        }
        url = reverse('lead-detail', args=(lead.pk,))
        response = client.patch(url, data, 'application/json')
        keys = {'phone', 'full_name', 'comment', 'lead_increment', 'status'}
        assert len(keys.difference(set(response.json()))) == 0
        assert data == response.json()
        assert response.status_code == status.HTTP_200_OK

    def test_delete_lead(self, client: Client, user, lead):
        client.force_login(user)
        url = reverse('lead-detail', args=(lead.pk,))
        count = Lead.objects.count()
        response = client.delete(url)
        assert Lead.objects.count() + 1 == count
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestArchiveModelViewSet:
    @pytest.fixture
    def user(self):
        user = User.objects.create_user(phone=1234567, password='pass')
        return user

    @pytest.fixture
    def archive(self):
        archive = Archive.objects.create(
            name="archive1"
        )
        return archive

    def test_archive_list(self, client: Client, user):
        client.force_login(user)
        url = reverse('archive_reasons-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert Archive.objects.count() == response.data['count']

    def test_create_archive(self, client: Client, user):
        client.force_login(user)
        data = {'name': 'new_archive_list'}
        url = reverse('archive_reasons-list')
        count = Archive.objects.count()
        response = client.post(url, data)
        assert Archive.objects.count() - 1 == count
        assert response.data['name'] == data['name']
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_archive(self, client: Client, user, archive):
        client.force_login(user)
        data = {'name': 'updated_archive_list'}
        url = reverse('archive_reasons-detail', args=(archive.pk,))
        response = client.put(url, data, 'application/json')
        assert response.data['name'] == data['name']
        assert response.status_code == status.HTTP_200_OK

    def test_patch_archive(self, client: Client, user, archive):
        client.force_login(user)
        data = {'name': 'patched_archive_list'}
        url = reverse('archive_reasons-detail', args=(archive.pk,))
        response = client.patch(url, data, 'application/json')
        assert response.data['name'] == data['name']
        assert response.status_code == status.HTTP_200_OK

    def test_delete_archive(self, client: Client, user, archive):
        client.force_login(user)
        url = reverse('archive_reasons-detail', args=(archive.pk,))
        count = Archive.objects.count()
        response = client.delete(url)
        assert Archive.objects.count() + 1 == count
        assert response.status_code == status.HTTP_204_NO_CONTENT
