from rest_framework.serializers import ModelSerializer

from groups.models import Course


class CourseListModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'image', 'description', 'lesson_duration', 'course_duration', 'price')


class CourseCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        read_only_fields = ('id',)
        fields = 'name', 'price', 'description', 'image', 'lesson_duration', 'course_duration', 'company'
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'description': {'required': False},
            'lesson_duration': {'required': True},
            'course_duration': {'required': True},
            'company': {'required': True},
            'image': {'allow_null': True, 'required': False}
        }
