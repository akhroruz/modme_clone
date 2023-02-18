# import pytest
# from django.contrib.auth.models import Group
#
# from groups.models import Company, Branch
# from users.models import User
#
#
# @pytest.mark.django_db
# class TestUser:
#     @pytest.fixture
#     def role(self):
#         return Group.objects.create(
#             name='teacher 1'
#         )
#
#     @pytest.fixture
#     def company(self):
#         return Company.objects.create(
#             name='company 1'
#         )
#
#     @pytest.fixture
#     def branch(self, company):
#         return Branch.objects.create(
#             name='branch 1',
#             address='address 1',
#             company_id=company.pk,
#             phone='934923327',
#         )
#
#     @pytest.fixture
#     def user(self, role, branch):
#         return User.objects.create_user(
#             phone='934923327',
#             first_name='Name 1',
#             last_name='Lastname 2',
#             password='1'
#         )
#
#     def test_create_user(self, user):
#         pass
