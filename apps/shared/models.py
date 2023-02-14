import uuid

from django.db.models import Model, UUIDField, DateTimeField


class UUIDBaseModel(Model):
    uuid = UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseModel(Model):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)
