import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from groups.models import Company
from users.models import Blog, User


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
    def blog(self, user, client: Client, company):
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

    def test_list_blogs(self, client: Client, user, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_retrieve(self, client: Client, user, rf, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-list'), company.pk)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create(self, client: Client, user, company):
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

    def test_update(self, client: Client, user, blog, company):
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
        response = client.put(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Updated Blog Title'
        assert response.data['text'] == 'Updated Blog Text'
        assert response.data['public']
        assert response.data['visible_all']
        assert response.data['view_count'] == 30

    def test_patch(self, client: Client, user, blog, company):
        client.force_login(user)
        data = {
            'title': 'Patched Blog Title',
            'text': 'Patched Blog Text',
            'public': False,
            'visible_all': False,
            'view_count': 55,

        }
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.patch(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Patched Blog Title'
        assert response.data['text'] == 'Patched Blog Text'
        assert not response.data['public']
        assert not response.data['visible_all']
        assert response.data['view_count'] == 55

    def test_delete(self, client: Client, user, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


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
