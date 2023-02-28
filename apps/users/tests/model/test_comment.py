import pytest
from django.contrib.contenttypes.models import ContentType
from users.models import User, Comment


@pytest.mark.django_db
class TestCommentModel:
    def test_create_comment(self):
        content_type = ContentType.objects.get_for_model(User)
        data = {
            'text': 'test_text',
            'content_type': content_type,
            'object_id': 1
        }
        comment_count = Comment.objects.count()
        comment = Comment.objects.create(**data)
        assert comment.text == data['text']
        assert comment.object_id == data['object_id']
        assert comment_count + 1 == Comment.objects.count()
