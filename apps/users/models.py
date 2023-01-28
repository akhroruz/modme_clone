from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, ManyToManyField, SET_NULL, \
    ForeignKey, DateTimeField

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
    role = ManyToManyField('groups.Role')
    branch = ForeignKey('groups.Branch', SET_NULL, null=True)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)
    password = CharField(max_length=255,)
    confirm_password = CharField(max_length=255,)

    EMAIL_FIELD = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return f'{self.phone}'
