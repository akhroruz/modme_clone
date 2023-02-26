import pytest

from groups.models import Company, Course


@pytest.mark.django_db
class TestCourseModel:
    def test_create_course(self):
        company = Company.objects.create(name='test_name')

        data = {
            'name': 'test_name',
            'price': 500,
            'description': 'test_description',
            'image': 'test_image.png',
            'lesson_duration': 3,
            'course_duration': 6,
            'company': company
        }
        course_count = Course.objects.count()
        course = Course.objects.create(**data)
        assert course.name == data['name']
        assert course.price == data['price']
        assert course.description == data['description']
        assert course.image == data['image']
        assert course.lesson_duration == data['lesson_duration']
        assert course.course_duration == data['course_duration']
        assert course.company == company
        assert str(course) == course.name
        assert course_count == Company.objects.count() - 1
