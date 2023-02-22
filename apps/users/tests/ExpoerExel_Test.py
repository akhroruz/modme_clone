# import pytest
# from django.test import Client
# from django.urls import reverse
# from rest_framework import status
# import pandas as pd
# from shared.utils.export_excel import export_data_excel
# from users.models import User, Comment
#
#
# # TODO: ahror_oka
# @pytest.mark.django_db
# class TestExportExcel:
#
#     @pytest.fixture
#     def user(self):
#         user = User.objects.create_user(
#             phone='1234567',
#             password='pass'
#         )
#         return user
#
#     def test_export_users_to_excel(self, client: Client, user):
#         client.force_login(user)
#         url = reverse('export')
#         response = client.get(url)
#         assert response.status_code == 200
#         comment = Comment.objects.create(text='My comment', user=user)
#         User.objects.create(first_name='John', phone='1234567', birth_date='2003-10-10', balance=100,
#                             comment_set=[comment])
#         columns = ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']
#         rows = User.objects.values_list('id', 'first_name', 'phone', 'birth_date', 'comment', 'balance')
#         response = export_data_excel(columns, rows)
#
#         assert response.status_code == status.HTTP_200_OK
#         assert response['Content-Type'] == 'application/ms-excel'
#         assert response['Content-Disposition'] == 'attachment; filename="books.xlsx"'
#
#         content = response.content
#         df = pd.read_excel(content, sheet_name='Users')
#
#         assert list(df.columns) == ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']
