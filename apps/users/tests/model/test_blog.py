from datetime import time

import pytest

from groups.models import Company
from users.models import User, Blog


@pytest.mark.django_db
class TestBlogModel:

    def test_create_blog(self):
        company_data = {
            'name': 'PDP',
            'logo': 'test_logo.png',
            'colors': 'Red',
            'start_working_time': time(hour=9, minute=00, second=00),
            'end_working_time': time(hour=12, minute=00, second=00),
            'phone': '991212334',
            'company_oferta': 'test_logo.png'
        }
        company = Company.objects.create(**company_data)
        user_data = {'phone': 1234567, 'password': 'pass'}
        user = User.objects.create_user(**user_data)

        blog_count = Blog.objects.count()
        blog_data = {
            'title': 'test_title',
            'text': 'test_text',
            'public': True,
            'created_by': user,
            'updated_by': user,
            'visible_all': True,
            'view_count': 100,
            'company': company
        }
        blog = Blog.objects.create(**blog_data)
        assert blog.title == blog_data['title']
        assert blog.text == blog_data['text']
        assert blog.public
        assert blog.created_by == user
        assert blog.updated_by == user
        assert blog.visible_all
        assert blog.view_count == blog_data['view_count']
        assert blog.company == company
        assert str(blog) == blog.title
        assert blog_count + 1 == Blog.objects.count()
        assert len(blog.__dict__) - len(blog_data) == 4
