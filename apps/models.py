from django.db.models import IntegerField, CharField, Model, ImageField, TextField

from shared.models import BaseModel


class Role(BaseModel):
    name = CharField(max_length=255)

    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Role'


class Branch(BaseModel):
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    phone_number = IntegerField(unique=True)
    about = TextField()
    image = ImageField(max_length=100, upload_to='images/')

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branch'
