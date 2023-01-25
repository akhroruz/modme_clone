from django.db.models import IntegerField, CharField, Model, ImageField, TextField, ForeignKey, SET_NULL, TextChoices, \
    TimeField

from shared.models import BaseModel


class Role(BaseModel):
    name = CharField(max_length=255)


class Branch(BaseModel):
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    phone_number = IntegerField(unique=True)
    about = TextField()
    image = ImageField(max_length=100, upload_to='images/')


class Room(BaseModel):
    name = CharField(max_length=255)


class Course(Model):
    name = CharField(max_length=255)


# class Group(BaseModel):
#     class DaysChoice(TextChoices):
#         ODD_DAYS = 'odd_days', 'Odd days'
#         EVEN_DAYS = 'even days', 'Even Days'
#         DAY_OFF = 'day_off', 'Day off'
#
#     name = CharField(max_length=255)
#     teacher = ForeignKey('users.User', SET_NULL, null=True)
#     start_time = TimeField(null=True, blank=True)
