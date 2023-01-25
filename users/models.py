from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, ManyToManyField, SET_NULL, \
    ForeignKey, DateTimeField

from users.managers import MyUserManager


class User(AbstractBaseUser):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    full_name = CharField(max_length=64)
    phone_number = IntegerField(unique=True)
    birth = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/profile.jpg', blank=True, null=True)
    role = ManyToManyField('apps.Role')
    branch = ForeignKey('apps.Branch', SET_NULL, null=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

