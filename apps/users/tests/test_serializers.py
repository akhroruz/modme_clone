import pytest

from shared.tests import TestBaseFixture


@pytest.mark.django_db
class TestUserListModelSerializer(TestBaseFixture):
    pass
    # def test_user_list(self, client, user, branch, role):
    #     client.force_login(user)
    #     url = '%s?branch=%s&user_type=%s' % (reverse('user-list'), branch.pk, role.name)
    #     response = client.get(url)
    #     assert response.status_code == status.HTTP_200_OK
    #     assert User.objects.count() == response.data['count']
