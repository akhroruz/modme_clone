import pytest

from groups.models import Company, Branch, Room


@pytest.mark.django_db
class TestRoomModel:

    def test_room(self):
        company = Company.objects.create(name='PDP')
        branch = Branch.objects.create(
            name='test branch',
            address='test branch address',
            phone='934341245',
            about='test branch about',
            image='branch_image/.png',
            company=company
        )
        room_count = Room.objects.count()
        data = {'name': 'test_room', 'branch': branch}
        room = Room.objects.create(**data)

        assert room.name == data['name']
        assert room.branch == branch
        assert str(room) == room.name
        assert room_count == Room.objects.count() - 1
