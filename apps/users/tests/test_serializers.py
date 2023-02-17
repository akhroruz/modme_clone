import pytest
from django.contrib.auth.models import Group as Role
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.reverse import reverse

from core.settings import MEDIA_ROOT
from groups.models import Company, Group, Branch, Room
from users.models import User, Archive


# @pytest.mark.django_db
# class TestBlogModelSerializer:
#
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(
#             name='Company 1',
#         )
#         return company
#
#     @pytest.fixture
#     def user(self):
#         user = User.objects.create_user(phone=1234567, password='pass')
#         return user
#
#     @pytest.fixture
#     def blog(self, user, client: Client, company):
#         blog = Blog.objects.create(
#             title='Blog 1',
#             text='Text 1',
#             public=True,
#             created_by=user,
#             updated_by=user,
#             visible_all=True,
#             view_count=11,
#             company=company
#         )
#         return blog
#
#     def test_list_blogs(self, client: Client, user, blog, company):
#         client.force_login(user)
#         url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
#         response = client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) == 4
#
#     def test_retrieve(self, client: Client, user, rf, blog, company):
#         client.force_login(user)
#         url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
#         response = client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_create(self, client: Client, user, company):
#         client.force_login(user)
#         data = {
#             'title': 'New Blog Title',
#             'text': 'New Blog Text',
#             'public': False,
#             'visible_all': False,
#             'view_count': 20,
#             'company': company.pk
#         }
#         url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
#         response = client.post(url, data)
#         assert response.status_code == status.HTTP_201_CREATED
#
#     def test_update(self, client: Client, user, blog, company):
#         client.force_login(user)
#         data = {
#             'title': 'Updated Blog Title',
#             'text': 'Updated Blog Text',
#             'public': True,
#             'visible_all': True,
#             'view_count': 30,
#             'company': company.pk
#
#         }
#         url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
#         response = client.put(url, data, 'application/json')
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['title'] == 'Updated Blog Title'
#         assert response.data['text'] == 'Updated Blog Text'
#         assert response.data['public']
#         assert response.data['visible_all']
#         assert response.data['view_count'] == 30
#
#     def test_patch(self, client: Client, user, blog, company):
#         client.force_login(user)
#         data = {
#             'title': 'Patched Blog Title',
#             'text': 'Patched Blog Text',
#             'public': False,
#             'visible_all': False,
#             'view_count': 55,
#
#         }
#         url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
#         response = client.patch(url, data, 'application/json')
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['title'] == 'Patched Blog Title'
#         assert response.data['text'] == 'Patched Blog Text'
#         assert not response.data['public']
#         assert not response.data['visible_all']
#         assert response.data['view_count'] == 55
#
#     def test_delete(self, client: Client, user, blog, company):
#         client.force_login(user)
#         url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
#         response = client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestUserModelSerializer:

    @pytest.fixture
    def company(self):
        company = Company.objects.create(
            name='Company1 PDP',
        )
        return company

    @pytest.fixture
    def branch(self, company):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        branch = Branch.objects.create(
            name='branch1',
            address='address1',
            company_id=company.pk,
            phone='1234567',
            image=image
        )
        return branch

    @pytest.fixture
    def create_group(self, faker, branch):
        room = Room.objects.create(name=faker.first_name(), branch=branch)
        group = Group.objects.create(
            name=faker.first_name(),
            days=Group.DaysChoice.ODD_DAYS,
            room=room,
            branch=branch,
            tags=['tag1', 'tag2']
        )
        return group

    @pytest.fixture
    def archive(self):
        archive = Archive.objects.create(
            name='ARCHIVE SITY'
        )
        return archive

    @pytest.fixture
    def user(self, archive, create_group, teacher_role, branch):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        user = User.objects.create_user(
            phone=12345678,
            is_archive=False,
            archive_id=archive.pk,
            birth_date='2004-10-10',
            photo=image,
            balance=2,
            data={'JSON DATA': 'asa'},
            password='password',
        )
        user.branch.add(branch)
        user.role.add(teacher_role)
        user.save()
        return user

    @pytest.fixture
    def teacher_role(self):
        teacher = Role.objects.create(
            name='teacher'
        )
        return teacher

    def test_user_list(self, client, user, branch, teacher_role):
        client.force_login(user)
        url = '%s?branch=%s&user_type=%s' % (reverse('user-list'), branch.pk, teacher_role.name)
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 4

    def test_create(self, client, user, archive, branch, teacher_role):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        client.force_login(user)
        data = {
            'phone': '77777777',
            'archive_id': archive.pk,
            'birth_date': '2000-01-01',
            'balance': 45,
            'gender': user.GenderChoose.MALE,
            'role': teacher_role.pk,
            'branch': branch.pk,
            'password': 'password',
            'photo': image
        }

        url = '%s?branch=%s' % (reverse('user-list'), branch.pk)
        response = client.post(url, data)
        assert response.status_code == 201
        assert response.data['phone'] == '77777777'
        assert response.data['gender'] == user.GenderChoose.MALE
        assert response.data['birth_date'] == '2000-01-01'

    def test_update(self, client: Client, user, branch, teacher_role):
        client.force_login(user)
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        data = {
            'phone': 123456789,
            'birth_date': '1000-01-01',
            'balance': 100,
            'gender': user.GenderChoose.FEMALE,
            'password': '1234567890',
            'role': teacher_role.pk,
            'photo': image
        }
        url = reverse('user-detail', args=(user.pk,)) + f'?branch={branch.pk}&user_type={teacher_role.name}'
        response = client.put(url, data, content_type='multipart/form-data')
        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200 but got {response.status_code}"
        assert 'phone' in response.data, "Response data should contain 'phone' field"
        assert response.data['phone'] == 123456789, "Response data 'phone' field should match sent data"
        assert 'gender' in response.data, "Response data should contain 'gender' field"
        assert response.data[
                   'gender'] == user.GenderChoose.FEMALE, "Response data 'gender' field should match sent data"
        assert 'birth_date' in response.data, "Response data should contain 'birth_date' field"
        assert response.data['birth_date'] == '1000-01-01', "Response data 'birth_date' field should match sent data"
