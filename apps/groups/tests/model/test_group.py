from datetime import date, time

import pytest

from groups.models import Company, Branch, Room, Course, Group
from users.models import User


@pytest.mark.django_db
class TestGroupModel:
    def test_group(self):
        company = Company.objects.create(name='test_company')
        branch = Branch.objects.create(
            name='test branch',
            address='test branch address',
            phone='934341245',
            about='test branch about',
            image='branch_image.png',
            company=company
        )
        room = Room.objects.create(name='test_room', branch=branch)
        course = Course.objects.create(
            name='test_name',
            price=1500,
            description='test_description',
            image='test_image.png',
            lesson_duration=2,
            course_duration=6,
            company=company
        )
        user = User.objects.create_user(phone='1233434', password='test_password')

        group_data = {
            'name': 'test_name',
            'days': 'Odd days',
            'status': 'active',
            'room': room,
            'teacher': user,
            'start_time': time(hour=9, minute=00),
            'end_time': time(hour=12, minute=30),
            'course': course,
            'branch': branch,
            'start_date': date(2023, 2, 23),
            'end_date': date(2023, 5, 23),
            'tags': ['test_tag1']
        }
        group_count = Group.objects.count()
        group = Group.objects.create(**group_data)
        group.students.add(user)

        assert group.name == group_data['name']
        assert group.days == group_data['days']
        assert group.status == group_data['status']
        assert group.room == room
        assert group.start_time == group_data['start_time']
        assert group.end_time == group_data['end_time']
        assert group.course == course
        assert group.branch == branch
        assert group.start_date == group_data['start_date']
        assert group.end_date == group_data['end_date']
        assert group.tags == group_data['tags']
        assert group_count + 1 == Group.objects.count()
