import pytest
from django.contrib.auth.models import Group as Role
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.test.client import BOUNDARY, MULTIPART_CONTENT, encode_multipart  # noqa
from rest_framework import status
from rest_framework.reverse import reverse

from core.settings import MEDIA_ROOT
from groups.models import Company, Group, Branch, Room
from users.models import User, Archive, Blog, LeadIncrement, Lead


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

    def test_delete_blog(self, client: Client, user, blog, company):
        client.force_login(user)
        url = '%s?company=%s' % (reverse('news_blog-detail', args=(blog.pk,)), company.pk)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


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
            name='Archive city'
        )
        return archive

    @pytest.fixture
    def role(self):
        role = Role.objects.create(
            name='teacher'
        )
        return role

    @pytest.fixture
    def user(self, archive, create_group, role, branch):
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
        user.role.add(role)
        user.save()
        return user

    def test_user_list(self, client, user, branch, role):
        client.force_login(user)
        url = '%s?branch=%s&user_type=%s' % (reverse('user-list'), branch.pk, role.name)
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data) == 4

    def test_create(self, client, user, archive, branch, role):
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        client.force_login(user)
        data = {
            'phone': '934923327',
            'archive_id': archive.pk,
            'birth_date': '2000-01-01',
            'balance': 45,
            'gender': user.GenderChoose.MALE,
            'role': role.pk,
            'branch': branch.pk,
            'password': 'password',
            'photo': image
        }

        url = '%s?branch=%s' % (reverse('user-list'), branch.pk)
        response = client.post(url, data)
        assert response.status_code == 201
        assert response.data['phone'] == data['phone']
        assert response.data['gender'] == user.GenderChoose.MALE
        assert response.data['birth_date'] == data['birth_date']

    def test_update(self, client: Client, user, branch, role):
        client.force_login(user)
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', open(image_path, 'rb').read(), 'image/png')

        data = {
            'birth_date': '1999-01-11',
            'password': '1234567890',
            'role': role.pk,
            'photo': image,
            'gender': user.GenderChoose.FEMALE
        }

        url = reverse('user-detail', args=(user.pk,)) + f'?branch={branch.pk}&user_type={role.name}'
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)

        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200 but got {response.status_code}"
        assert 'gender' in response.data, "Response data should contain 'gender' field"
        assert response.data['gender'] == user.GenderChoose.FEMALE, "Response data 'gender' " \
                                                                    "field should match sent data"
        assert 'birth_date' in response.data, "Response data should contain 'birth_date' field"
        assert response.data['birth_date'] == data[
            'birth_date'], "Response data 'birth_date' field should match sent data"

    def test_patch(self, client: Client, user, branch, role):
        client.force_login(user)
        image_path = MEDIA_ROOT + '/test.png'
        image = SimpleUploadedFile('test.png', open(image_path, 'rb').read(), 'image/png')

        data = {
            'birth_date': '1000-10-10',
            'password': 'password1',
            'role': role.pk,
            'photo': image,
            'gender': user.GenderChoose.MALE
        }

        url = reverse('user-detail', args=(user.pk,)) + f'?branch={branch.pk}&user_type={role.name}'
        response = client.put(url, encode_multipart(BOUNDARY, data), MULTIPART_CONTENT)

        assert response.status_code == status.HTTP_200_OK, f"Expected status code 200 but got {response.status_code}"
        assert 'gender' in response.data, "Response data should contain 'gender' field"
        assert response.data['gender'] == user.GenderChoose.MALE, "Response data 'gender' " \
                                                                  "field should match sent data"
        assert 'birth_date' in response.data, "Response data should contain 'birth_date' field"
        assert response.data['birth_date'] == data['birth_date'], \
            "Response data 'birth_date' field should match sent data"

    def test_delete_user(self, client: Client, user, branch, role, company):
        client.force_login(user)
        url = reverse('user-detail', args=(user.pk,)) + f'?branch={branch.pk}&user_type={role.name}'
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestLeadIncrementSerialize:
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
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_retrieve(self, client: Client, user):
        client.force_login(user)
        url = reverse('lead_increment-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_lead_increment(self, client: Client, user):
        client.force_login(user)
        data = {
            'name': '_Increment',
        }
        url = reverse('lead_increment-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_lead_increment(self, client: Client, user, lead_increment):
        client.force_login(user)
        data = {
            'name': 'updated_new_increment',
        }
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        response = client.put(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'updated_new_increment'

    def test_patch_lead_increment(self, client: Client, user, lead_increment):
        client.force_login(user)
        data = {
            'name': 'PATCHED_Increment',
        }
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        response = client.put(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'PATCHED_Increment'

    def test_delete_lead_increment(self, client: Client, user, lead_increment):
        client.force_login(user)
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestLeadSerializer:

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
            lead_increment_id=lead_increment.pk,
            status=Lead.LeadStatus.REQUESTS
        )
        return lead

    def test_lead_list(self, client: Client, user):  # noqa
        client.force_login(user)
        url = reverse('lead-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_lead_retrieve(self, client: Client, user):  # noqa
        client.force_login(user)
        url = reverse('lead-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_lead(self, client: Client, user, lead, lead_increment):  # noqa
        client.force_login(user)
        data = {
            'phone': 7777777,
            'full_name': 'Botirali',  # noqa
            'comment': 'botirali commentti',  # noqa
            'lead_increment': lead_increment.pk,
            'status': Lead.LeadStatus.PENDING
        }
        url = reverse('lead-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_lead(self, client: Client, user, lead, lead_increment):
        client.force_login(user)
        data = {
            'phone': 9999999,
            'full_name': 'Updated_full_name',
            'comment': 'Updated_comment',
            'lead_increment': lead_increment.pk,
            'status': Lead.LeadStatus.COLLECT
        }
        url = reverse('lead-detail', args=(lead.pk,))
        response = client.put(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == 'Updated_full_name'
        assert response.data['comment'] == 'Updated_comment'
        assert response.data['status'] == Lead.LeadStatus.COLLECT

    def test_patch_lead(self, client: Client, user, lead, lead_increment):
        client.force_login(user)
        data = {
            'phone': 7777777,
            'full_name': 'PATCHED_full_name',  # noqa
            'comment': 'PATCHED_comment',  # noqa
            'lead_increment': lead_increment.pk,
            'status': Lead.LeadStatus.PENDING
        }
        url = reverse('lead-detail', args=(lead.pk,))
        response = client.patch(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['full_name'] == 'PATCHED_full_name'
        assert response.data['comment'] == 'PATCHED_comment'
        assert response.data['status'] == Lead.LeadStatus.PENDING

    def test_delete_lead(self, client: Client, user, lead):
        client.force_login(user)
        url = reverse('lead-detail', args=(lead.pk,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestArchiveSerializer:
    @pytest.fixture  # noqa
    def user(self):
        user = User.objects.create_user(phone=1234567, password='pass')
        return user

    @pytest.fixture
    def archive(self):
        archive = Archive.objects.create(
            name="ARCHIVE1"
        )
        return archive

    def test_archive_list(self, client: Client, user):  # noqa
        client.force_login(user)
        url = reverse('archive_reasons-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 4

    def test_retrieve_archive(self, client: Client, user):  # noqa
        client.force_login(user)
        url = reverse('archive_reasons-list')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_lead_increment(self, client: Client, user, archive):  # noqa
        client.force_login(user)
        data = {
            'name': 'New_arxiv_qora_royxat ',  # noqa
        }
        url = reverse('archive_reasons-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_update_archive(self, client: Client, user, archive):  # noqa
        client.force_login(user)
        data = {
            'name': 'Updated New archive OQ ROYXAT'  # noqa
        }
        url = reverse('archive_reasons-detail', args=(archive.pk,))
        response = client.put(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Updated New archive OQ ROYXAT'  # noqa

    def test_patch_archive(self, client: Client, user, archive):  # noqa
        client.force_login(user)
        data = {
            'name': 'PATCHED New archive OQ ROYXAT'  # noqa
        }
        url = reverse('archive_reasons-detail', args=(archive.pk,))
        response = client.put(url, data, 'application/json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'PATCHED New archive OQ ROYXAT'  # noqa

    def test_delete_archive(self, client: Client, user, archive):  # noqa
        client.force_login(user)
        url = reverse('archive_reasons-detail', args=(archive.pk,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
