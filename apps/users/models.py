from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, ManyToManyField, JSONField, \
    TextField, DateTimeField

from apps.users.managers import MyUserManager


class User(AbstractUser):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    email = None
    username = None
    full_name = CharField(max_length=64)
    phone = IntegerField(unique=True)
    birth = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/profile.jpg', blank=True, null=True)
    balance = IntegerField(default=0, null=True, blank=True)
    group = ManyToManyField('groups.Group')
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
        return f'{self.full_name}:{self.phone}'


