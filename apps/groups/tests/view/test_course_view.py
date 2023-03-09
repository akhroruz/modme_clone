import pytest
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework import status
from rest_framework.reverse import reverse

from groups.models import Course
from shared.tests import TestBaseFixture


@pytest.mark.django_db
class TestCourseModelViewSet(TestBaseFixture):

    def test_course_list(self, user, client: Client, company, course):
        keys = {'id', 'name', 'image', 'description', 'lesson_duration', 'course_duration', 'price'}
        client.force_login(user)
        url = reverse('course-list') + f'?company={company.pk}'
        response = client.get(url)  # noqa
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == Course.objects.count()
        item = response.data['results'][0]
        assert len(keys.difference(set(item))) == 0  # noqa

    def test_create_course(self, user, client, course):
        client.force_login(user)
        data = {
            'name': 'New Created Course',
            'price': 500000,
            'description': 'text description',
            'lesson_duration': 2,
            'course_duration': 30,
            'company': course.company.pk,
        }
        url = reverse('course-list') + f'?company={course.company.pk}'
        previous_count = Course.objects.count()
        response = client.post(url, data)
        item = response.json()
        assert previous_count + 1 == Course.objects.count()
        keys = {'name', 'description', 'price', 'lesson_duration', 'course_duration', 'company'}
        assert len(keys.difference(set(item))) == 0  # noqa
        item.pop('image', None)  # noqa
        assert data == item
        assert response.status_code == status.HTTP_201_CREATED

    def test_course_update(self, client, user, course):
        client.force_login(user)
        data = {
            'name': 'Updated Course',
            'price': 777,
            'description': 'updated description',
            'lesson_duration': 4,
            'course_duration': 44,
            'company': course.company.pk,
        }

        url = reverse('course-detail', args=(course.pk,)) + f'?company={course.company.pk}'
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        item = response.json()
        keys = {'name', 'price', 'description', 'lesson_duration', 'course_duration', 'company'}
        assert len(keys.difference(set(item))) == 0  # noqa
        item.pop('image', None)  # noqa
        data.pop('image', None)
        assert data == item
        assert response.status_code == status.HTTP_200_OK

    def test_course_update_partial(self, client, user, course):
        client.force_login(user)
        data = {
            'name': 'patched course',
            'price': 660,
            'company': course.company.pk,
        }

        url = reverse('course-detail', args=(course.pk,)) + f'?company={course.company.pk}'
        response = client.patch(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)
        item = response.json()
        keys = {'name', 'price', 'company'}
        assert len(keys.difference(set(item))) == 0  # noqa
        for key, value in data.items():
            assert item[key] == value
        assert response.status_code == status.HTTP_200_OK

    def test_delete_course(self, client, user, course):
        client.force_login(user)
        url = reverse('course-detail', args=(course.pk,)) + f'?company={course.company.pk}'
        previous_count = Course.objects.count()
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert previous_count - 1 == Course.objects.count()
