# import pytest
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
# from django.test import Client
# from rest_framework import status
# from rest_framework.reverse import reverse
#
# from users.models import LeadIncrement, Lead, User, Blog
#
#
# @pytest.mark.django_db
# class TestLeadModelViewSet:
#
#     @pytest.fixture
#     def lead_increment(self):
#         lead_increment = LeadIncrement.objects.create(
#             name='Lead 1'
#         )
#         return lead_increment
#
#     @pytest.fixture
#     def lead(self, lead_increment):
#         return Lead.objects.create(
#             full_name='full name 1',
#             comment='comment 1',
#             phone='990675624',
#             status=Lead.LeadStatus.REQUESTS,
#             lead_increment=lead_increment
#         )

#     def test_list_lead(self, client: Client, lead):
#         url = reverse('lead-list')
#         response = client.get(url)
#         item = response.data['results'][0]
#         assert response.status_code == status.HTTP_200_OK
#         assert item['full_name'] == lead.full_name
#         assert item['comment'] == lead.comment
#         assert item['phone'] == lead.phone
#         assert item['status'] == lead.status
#         assert item['lead_increment'] == lead.lead_increment_id
#
#     def test_create_lead(self, client: Client, lead):
#         url = reverse('lead-list')
#         data = {
#             'full_name': lead.full_name,
#             'comment': lead.comment,
#             'phone': lead.phone,
#             'status': lead.status,
#             'lead_increment': lead.lead_increment_id
#         }
#         response = client.post(url, data, 'application/json')
#         item = response.json()
#         assert response.status_code == status.HTTP_201_CREATED
#
#         assert item['full_name'] == data['full_name']
#         assert item['comment'] == data['comment']
#         assert item['phone'] == data['phone']
#         assert item['status'] == data['status']
#         assert item['lead_increment'] == data['lead_increment']
#
#     def test_update_lead(self, client: Client, lead):
#         url = reverse('lead-detail', args=[lead.id])
#         data = {
#             'full_name': lead.full_name,
#             'comment': lead.comment,
#             'phone': lead.phone,
#             'status': lead.status,
#             'lead_increment': lead.lead_increment_id
#         }
#         response = client.put(url, data, 'application/json')
#         item = response.data
#
#         assert response.status_code == status.HTTP_200_OK
#         assert item['full_name'] == data['full_name']
#         assert item['comment'] == data['comment']
#         assert item['phone'] == data['phone']
#         assert item['status'] == data['status']
#         assert item['lead_increment'] == data['lead_increment']
#
#     def test_delete_lead(self, client: Client, lead):
#         url = reverse('lead-detail', args=[lead.id])
#         response = client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#
# @pytest.mark.django_db
# class TestLeadIncrementModelVIewSet:
#
#     @pytest.fixture
#     def lead_increment(self):
#         return LeadIncrement.objects.create(
#             name='Lead Increment 1'
#         )
#
#     def test_list_lead_increment(self, client: Client, lead_increment):
#         url = reverse('lead_increment-list')
#         response = client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['results'][0]['name'] == lead_increment.name
#
#     def test_create_lead_increment(self, client: Client, lead_increment):
#         url = reverse('lead_increment-list')
#         data = {
#             'name': 'Lead Increment 1'
#         }
#         response = client.post(url, data, 'application/json')
#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['name'] == lead_increment.name
#
#     def test_update_lead_increment(self, client: Client, lead_increment):
#         url = reverse('lead_increment-detail', args=[lead_increment.id])
#         data = {
#             'name': 'Lead Increment 1'
#         }
#         response = client.put(url, data, 'application/json')
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data['name'] == lead_increment.name
#
#     def test_delete_lead_increment(self, client: Client, lead_increment):
#         url = reverse('lead_increment-detail', args=[lead_increment.id])
#         response = client.delete(url)
#         assert response.status_code == status.HTTP_204_NO_CONTENT
#
#
# User = get_user_model()
#
#
# @pytest.mark.django_db
# class TestBlogModelViewSet:
#     client = Client()
#
#     @pytest.fixture
#     def base_user(self):
#         user = User.objects.create_user(phone='123456789', password='password1')
#         Blog.objects.create(
#             title='Test Blog 1',
#             text='This is a test blog',
#             public=True,
#             created_by=user,
#             updated_by=user,
#             visible_all=True,
#             view_count=0
#         )
#         self.client.login(phone='123456789', password='password1')
#         return user
#
#     @pytest.fixture
#     def blog(self, base_user):
#         return Blog.objects.create(
#             title='Test Blog 1',
#             text='This is a test blog',
#             public=True,
#             created_by_id=base_user.pk,
#             updated_by_id=base_user.pk,
#             visible_all=True,
#             view_count=0
#         )
#
#     def test_retrieve_blog(self, base_user):
#         url = reverse('news_blog-detail', args=(1,))
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#         blog = Blog.objects.get(id=1)
#         assert blog.view_count == 1
#         assert blog.title == 'Test Blog 1'
#         assert blog.text == 'This is a test blog'
#         assert blog.public == True
#         assert blog.visible_all == True
#
#     def test_list_blogs(self, base_user):
#         url = reverse('news_blog-list')
#         response = self.client.get(url)
#         assert response.status_code == status.HTTP_200_OK
#
#     def test_create_blog(self, base_user):
#         data = {
#             'title': 'Test Blog 2',
#             'text': 'This is a test blog 2',
#             'public': True,
#             'visible_all': True
#         }
#         url = reverse('news_blog-list')
#         response = self.client.post(url, data=data)
#         blog = response.data
#         assert response.status_code == 201
#         assert blog.get('title') == 'Test Blog 2'
#         assert blog.get('text') == 'This is a test blog 2'
#         assert blog.get('public') == True
#         assert blog.get('visible_all') == True
#         assert blog.get('view_count') == 0
#
#     def test_update_blog(self, client, blog):
#         url = reverse('news_blog-detail', args=(blog.pk,))
#         data = {
#             'title': 'Test Blog 1 - updated',
#             'text': 'This is a test blog - updated',
#             'public': False,
#             'visible_all': False
#         }
#         response = self.client.put(url, data=data, content_type='application/json')
#         assert response.status_code == 200
