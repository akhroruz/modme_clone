import datetime
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart
import pytest
from django.test import Client
from rest_framework import status
from rest_framework.reverse import reverse

from groups.models import Group
from shared.tests import TestBaseFixture
from users.models import Archive, Blog, LeadIncrement, Lead


@pytest.mark.django_db
class TestBlogModelViewSet(TestBaseFixture):

    def test_list_blogs(self, client: Client, user, company, blog):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.get(url)
        assert Blog.objects.count() == response.data['count']
        assert response.status_code == status.HTTP_200_OK

    def test_create_blog(self, client: Client, user, company, blog):
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
class TestLeadIncrementModelViewSet(TestBaseFixture):

    def test_lead_increment_list(self, client: Client, user, lead_increment):
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
class TestLeadModelViewSet(TestBaseFixture):

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
class TestArchiveModelViewSet(TestBaseFixture):

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


@pytest.mark.django_db
class TestGroupViewSet(TestBaseFixture):

    @pytest.fixture
    def group(self, room, branch, course, user):
        group = Group.objects.create(
            name='Python',
            days=Group.DaysChoice.ODD_DAYS,
            room=room,
            start_time='14:00:00',
            end_time='16:00:00',
            course=course,
            branch=branch,
            start_date='2003-10-15',
            end_date='2003-10-17',
            tags=['tag1', 'tag2'],
            teacher=user
        )
        group.students.add(user)
        group.save()
        return group

    def test_group_list(self, client: Client, room, branch, course, user):
        client.force_login(user)
        url = reverse('group-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_group_create(self, client: Client, room, branch, course, user):
        client.force_login(user)
        data = {
            'name': 'Java',
            'days': Group.DaysChoice.ODD_DAYS,
            'room': room.pk,
            'teacher': [user.pk],
            'start_time': '10:00:00',
            'end_time': '12:00:00',
            'course': course.pk,
            'branch': branch.pk,
            'start_date': '2003-10-10',
            'end_date': '2003-10-12',
            'tags': ['tag1', 'tag2'],
            'students': [user.pk]
        }

        url = reverse('group-list')
        prev_count = Group.objects.count()
        response = client.post(url, data)
        group = Group.objects.last()
        assert data['branch'] == response.data['branch']
        assert group.course == course
        assert datetime.datetime.strptime(data['start_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'start_time']
        assert datetime.datetime.strptime(data['end_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'end_time']
        assert datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y-%m-%d') == response.data[
            'start_date']
        assert datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y-%m-%d') == response.data[
            'end_date']

        keys = {'name', 'days', 'start_time', 'end_time', 'start_date', 'end_date', 'tags', }
        x = response.json()
        assert len(keys.difference(set(x))) == 0
        for key in keys:
            assert data[key] == x[key]
        assert Group.objects.count() == prev_count + 1
        assert response.status_code == status.HTTP_201_CREATED

    def test_put_group(self, client: Client, group, room, branch, course, user):
        client.force_login(user)
        data = {
            'name': 'Python',
            'days': group.DaysChoice.EVEN_DAYS,
            'room': room.pk,
            'teacher': user.pk,
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'course': group.course.pk,
            'branch': branch.pk,
            'start_date': '2003-10-15',
            'end_date': '2003-10-17',
            'tags': ['tag3', 'tag4'],
            'students': [user.pk]
        }

        url = '%s?branch=%s' % (reverse('group-detail', args=[group.pk]), branch.pk)
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        group = Group.objects.last()
        assert data['branch'] == response.data['branch']
        assert group.course == course
        assert datetime.datetime.strptime(data['start_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'start_time']
        assert datetime.datetime.strptime(data['end_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'end_time']
        assert datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y-%m-%d') == response.data[
            'start_date']
        assert datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y-%m-%d') == response.data[
            'end_date']

        keys = {'name', 'days', 'start_time', 'end_time', 'start_date', 'end_date', 'tags', }
        x = response.json()
        assert len(keys.difference(set(x))) == 0
        for key in keys:
            assert data[key] == x[key]
        assert response.status_code == status.HTTP_200_OK

    def test_patch_group(self, client: Client, group, room, branch, course, user):
        client.force_login(user)
        data = {
            'name': 'CSS',
            'days': group.DaysChoice.EVEN_DAYS,
            'room': room.pk,
            'teacher': user.pk,
            'start_time': '14:00:00',
            'end_time': '16:00:00',
            'course': group.course.pk,
            'branch': branch.pk,
            'start_date': '2003-10-15',
            'end_date': '2003-10-17',
            'tags': ['tag3', 'tag4'],
            'students': [user.pk]
        }

        url = '%s?branch=%s' % (reverse('group-detail', args=[group.pk]), branch.pk)
        response = client.patch(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        group = Group.objects.last()
        assert data['branch'] == response.data['branch']
        assert group.course == course
        assert datetime.datetime.strptime(data['start_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'start_time']
        assert datetime.datetime.strptime(data['end_time'], '%H:%M:%S').strftime('%H:%M:%S') == response.data[
            'end_time']
        assert datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%Y-%m-%d') == response.data[
            'start_date']
        assert datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%Y-%m-%d') == response.data[
            'end_date']

        keys = {'name', 'days', 'start_time', 'end_time', 'start_date', 'end_date', 'tags', }
        x = response.json()
        assert len(keys.difference(set(x))) == 0
        for key in keys:
            assert data[key] == x[key]
        assert response.status_code == status.HTTP_200_OK

    def test_delete_group(self, client: Client, user, branch, group):
        client.force_login(user)
        url = '%s?branch=%s' % (reverse('group-detail', args=[group.pk]), branch.pk)
        prev_count = Group.objects.count()
        response = client.delete(url)
        assert Group.objects.count() + 1 == prev_count
        assert response.status_code == status.HTTP_204_NO_CONTENT
