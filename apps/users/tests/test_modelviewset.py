import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status
from shared.utils.export_excel import export_data_excel, export_users_to_excel
from users.models import User, LeadIncrement, Archive, Lead
import pandas as pd


@pytest.mark.django_db
class TestLeadIncrementModelViewSet:
    @pytest.fixture
    def user(self):
        user = User.objects.create_user(
            phone=7777,
            password='01A777DA'
        )
        return user

    @pytest.fixture
    def lead_increment(self):
        lead_increment = LeadIncrement.objects.create(
            name='lead_increment1',
        )
        return lead_increment

    def test_lead_increment_list(self, client: Client, user, lead_increment):
        client.force_login(user)
        url = reverse('lead_increment-list')
        response = client.get(url)
        assert response.status_code == 200
        assert str(lead_increment) == lead_increment.name

    def test_lead_increment_create(self, client: Client, user, lead_increment):
        client.force_login(user)
        data = {
            'name': 'New_Lead_increment'
        }
        url = reverse('lead_increment-list')
        response = client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == 'New_Lead_increment'

    def test_delete_lead_increment(self, client: Client, user, lead_increment):
        client.force_login(user)
        url = reverse('lead_increment-detail', args=(lead_increment.pk,))
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db  # noqa
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

    def test_lead_list(self, client: Client, user, lead):  # noqa
        client.force_login(user)
        url = reverse('lead-list')
        response = client.get(url)
        assert str(lead) == f"{lead.full_name} | {lead.phone}"
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

    def test_archive_list(self, client: Client, user, archive):  # noqa
        client.force_login(user)
        url = reverse('archive_reasons-list')
        response = client.get(url)
        assert str(archive) == str(archive.name)
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


@pytest.mark.django_db
class TestExportExcel:

    @pytest.fixture
    def user(self):
        user = User.objects.create_user(
            phone='5555555',
            password='password5',
        )
        return user

    @pytest.fixture
    def columns(self):
        return ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']

    @pytest.fixture
    def rows(self):
        return [
            [1, 'Gucci', '777-77-77', '2000-32-33', 'only top', 1000],
        ]

    @pytest.fixture
    def exported_file(self, client: Client, columns, rows, user):
        client.force_login(user)
        url = reverse('export-detail')
        response = client.get(url)
        assert response.status_code == 200
        return pd.read_excel(response.content)

    def test_export_users_to_excel(self):
        User.objects.create(first_name='Backend', phone='66666666')
        response = export_users_to_excel()

        assert response.status_code == 200
        assert response['Content-Type'] == 'application/ms-excel'
        assert response['Content-Disposition'] == 'attachment; filename="books.xlsx"'

        # Read exel from response
        content = response.content
        df = pd.read_excel(content)

        assert len(df) == 1
        assert list(df.columns) == ['first_name', 'phone']
        assert list(df.values[0]) == ['Backend', 66666666]
        # explanation [prosta yozb qoydm yaxshi narsa ekan]  # noqa
        '''
            >>> df = pd.DataFrame({'age':    [ 3,  29],
                                   'height': [94, 170],
                                   'weight': [31, 115]})
            >>> df
               age  height  weight
            0    3      94      31
            1   29     170     115
        '''

    def test_export_data_excel(self, columns, rows):
        response = export_data_excel(columns, rows)
        assert response.status_code == status.HTTP_200_OK
