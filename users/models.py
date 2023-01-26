from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, ManyToManyField, SET_NULL, \
    ForeignKey, DateTimeField

from users.managers import MyUserManager


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
    role = ManyToManyField('apps.Role')
    branch = ForeignKey('apps.Branch', SET_NULL, null=True)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)

    EMAIL_FIELD = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

