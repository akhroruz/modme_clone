import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from shared.tests import TestBaseFixture


# TODO: ahror_oka
@pytest.mark.django_db
class TestExportExcel(TestBaseFixture):

    def test_export_users_to_excel(self, client: Client, user):
        client.force_login(user)
        url = reverse('user-export')
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # comment = Comment.objects.create(
        #     text='My comment',
        #     content_type=ContentType.objects.get_for_model(get_user_model()),
        #     object_id=user.pk,
        # )
        # columns = ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']
        # rows = User.objects.values_list('id', 'first_name', 'phone', 'birth_date', 'comment', 'balance')
        # response = export_data_excel(columns, rows)
        # assert response['Content-Type'] == 'application/ms-excel'
        # assert response['Content-Disposition'] == 'attachment; filename="books.xlsx"'
        # content = response.content
        # df = pd.read_excel(content, sheet_name='Users')
        # assert list(df.columns) == ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']
