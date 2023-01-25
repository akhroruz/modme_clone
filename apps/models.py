from django.db.models import IntegerField, CharField, Model, ImageField, TextField

from shared.models import BaseModel


class Role(BaseModel):
    name = CharField(max_length=255)


class Branch(BaseModel):
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    phone_number = IntegerField(unique=True)
    about = TextField()
    image = ImageField(max_length=100, upload_to='images/')
