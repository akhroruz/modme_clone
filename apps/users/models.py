from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, JSONField, \
    TextField, DateTimeField, Model

from apps.users.managers import MyUserManager


class User(AbstractUser):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    email = None
    username = None
    phone = IntegerField(unique=True)
    birth_date = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/profile.jpg', blank=True, null=True)
    balance = IntegerField(default=0, null=True, blank=True)

    # student
    datas = JSONField(null=True, blank=True)
    comment = TextField(blank=True, null=True)  # izoh # noqa

    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    EMAIL_FIELD = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f'{self.phone}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


