import pytest
from django.contrib.auth.models import Group as Role
from django.core.files.uploadedfile import SimpleUploadedFile

from core.settings import MEDIA_ROOT
from groups.models import Branch, Company, Room
from groups.serializers import BranchModelSerializer, GroupModelSerializer, RoomCreateModelSerializer


# @pytest.mark.django_db
# class TestGroupModelSerializer:
#
#     @pytest.fixture
#     def group(self):
#         return Role.objects.create(name='Role 1')
#
#     def test_group_model_serializer(self, group):
#         serializer = GroupModelSerializer(group)
#         assert serializer.data['name'] == group.name
#
#
# @pytest.mark.django_db
# class TestBranchModelSerializer:
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(name='Company 1')
#         return company
#
#     @pytest.fixture
#     def branch(self, company):
#         image_path = MEDIA_ROOT + '/test.png'
#         image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
#
#         return Branch.objects.create(
#             name='Branch 1',
#             address='Address 1',
#             phone='990675624',
#             about='Text 1',
#             image=image,
#             company=company
#         )
#
#     def test_branch_model_serializer(self, branch):
#         serializer = BranchModelSerializer(branch)
#         assert serializer.data['name'] == branch.name
#         assert serializer.data['address'] == branch.address
#         assert serializer.data['phone'] == branch.phone
#         assert serializer.data['about'] == branch.about
#         assert serializer.data['image'] == branch.image.url
#         assert len(serializer.data) == 9
#
#
# @pytest.mark.django_db
# class TestRoomModelSerializer:
#
#     @pytest.fixture
#     def company(self):
#         company = Company.objects.create(name='Company 1')
#         return company
#
#     @pytest.fixture
#     def branch(self, company):
#         image_path = MEDIA_ROOT + '/test.png'
#         image = SimpleUploadedFile('test.png', content=open(image_path, 'rb').read(), content_type='image/jpeg')
#
#         return Branch.objects.create(
#             name='Branch 1',
#             address='Address 1',
#             phone='990675624',
#             about='Text 1',
#             image=image,
#             company=company
#         )
#
#     @pytest.fixture
#     def room(self, branch):
#         room = Room.objects.create(
#             name='Room 1',
#             branch=branch
#         )
#         return room
#
#     def test_room_model_serializer(self, room, branch):
#         serializer = RoomCreateModelSerializer(room)
#         assert serializer.data['name'] == room.name
#         assert serializer.data['branch'] == branch.pk
#         assert len(serializer.data) == 5

# @pytest.mark.django_db
# class TestStudentModelSerializer:
#     @pytest.fixture
#     def student_fixture(self):
#         return Branch.objects.create(
#             name='Branch 1',
#             address='Address 1',
#             phone=990675624,
#             about='Text 1',
#         )
#
#     @pytest.fixture
#     def room_fixture(self, branch_fixture):
#         return Room.objects.create(name='Room 1',
#                                    branch_id=branch_fixture.uuid)
#
#     def test_room_model_serializer(self, room_fixture, branch_fixture):
#         serializer = RoomCreateModelSerializer(room_fixture)
#         assert serializer.data['name'] == room_fixture.name
#         assert serializer.data['branch'] == branch_fixture.uuid
#
#         fields = ['phone', 'full_name', 'birth_date', 'gender', 'comment', 'datas', 'balance']
