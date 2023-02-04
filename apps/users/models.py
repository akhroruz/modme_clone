from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, ManyToManyField, JSONField, \
    TextField

from apps.users.managers import MyUserManager
from shared.models import BaseModel


class User(AbstractUser, BaseModel):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    email = None
    username = None
    full_name = CharField(max_length=64)  # ochirish kere!!!
    phone = IntegerField(unique=True)  # shumi charfiled qilish kere !?
    birth = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/profile.jpg', blank=True, null=True)
    balance = IntegerField(default=0, null=True, blank=True)
    group = ManyToManyField('groups.Group')
    password = CharField(max_length=255, )
    confirm_password = CharField(max_length=255, )  # ochirvorish kere !!!!
    # student
    datas = JSONField(null=True, blank=True)  # social accaunts urls
    comment = TextField(blank=True, null=True)  # izoh # noqa

    EMAIL_FIELD = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f'{self.full_name}:{self.phone}'
