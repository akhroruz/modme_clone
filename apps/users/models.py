from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, JSONField, \
    TextField, DateTimeField, Model, ManyToManyField, ForeignKey, CASCADE

from shared.models import BaseModel
from users.managers import MyUserManager


class User(AbstractUser, BaseModel):
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
    role = ManyToManyField('auth.Group', 'roles')

    # student
    datas = JSONField(null=True, blank=True)
    comment = TextField(blank=True, null=True)  # izoh # noqa

    deleted_at = DateTimeField(null=True)
    EMAIL_FIELD = None
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.phone}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Comment(BaseModel):
    text = TextField()
    user = ForeignKey('users.User', CASCADE, 'comments')


class Lid(BaseModel):
    full_name = CharField(max_length=255)
    comment = TextField()
    phone = IntegerField()
    lid_increment = ForeignKey('users.LidIncrement', CASCADE)

    def __str__(self):
        return f'{self.full_name} | {self.phone}'


class LidIncrement(BaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name
