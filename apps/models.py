import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import IntegerField, CharField, Model, DateTimeField, DateField, UUIDField, TextChoices, \
    ImageField, TextField, ForeignKey, ManyToManyField, CASCADE, SET_NULL
from django.utils.translation import gettext_lazy as _


class BaseModel(Model):
    uuid = UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class MyUserManager(BaseUserManager):

    def create_user(self, full_name, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have an phone number')
        user = self.model(
            full_name=full_name,
            phone_number=phone_number

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, full_name, phone_number, password):
        user = self.create_user(full_name, phone_number, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    full_name = CharField(_('full_name'), max_length=64)
    phone_number = IntegerField(_('phone_number'), unique=True)
    birth = DateField(_('birth_date'))
    gender = CharField(_('gender'), max_length=25, choices=GenderChoose.choices)
    photo = ImageField(_('photo_of_profile'), max_length=100, upload_to='profiles/', default='/media/profile.jpg')
    role = ManyToManyField('apps.Role', CASCADE)
    branch = ForeignKey('apps.Branch', SET_NULL, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['phone_number']

    objects = MyUserManager()

    class Meta:
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')

    def __str__(self) -> str:
        return str(self.phone_number)


class Role(BaseModel):
    name = CharField(_('role_name'), max_length=255)


class Branch(BaseModel):
    name = CharField(_('branch_name'), max_length=255)
    address = CharField(_('branch_location'), max_length=255)
    phone_number = IntegerField(_('phone_number_of_branch'), unique=True)
    about = TextField()
    image = ImageField(max_length=100, upload_to='images/')
