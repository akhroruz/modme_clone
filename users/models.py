from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, ManyToManyField, CASCADE, \
    SET_NULL, ForeignKey
from django.utils.translation import gettext_lazy as _


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


class User(AbstractUser):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    full_name = CharField(max_length=64)
    phone_number = IntegerField(unique=True)
    birth = DateField()
    gender = CharField(_('gender'), max_length=25, choices=GenderChoose.choices)
    photo = ImageField(max_length=100, upload_to='profiles/', default='/media/profile.jpg')
    role = ManyToManyField('apps.Role', CASCADE)
    branch = ForeignKey('apps.Branch', SET_NULL, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = 'phone_number',

    objects = MyUserManager()

    class Meta:
        verbose_name = _('Manager')
        verbose_name_plural = _('Managers')

    def __str__(self) -> str:
        return str(self.phone_number)
