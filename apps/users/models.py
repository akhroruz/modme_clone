from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, JSONField, \
    TextField, DateTimeField, Model, ManyToManyField, ForeignKey, CASCADE, BooleanField, SET_NULL

from shared.models import BaseModel, UUIDBaseModel
from users.managers import MyUserManager


class Archive(BaseModel):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    email = None
    username = None
    phone = CharField(max_length=15, unique=True)
    is_archive = BooleanField(default=False)
    archive = ForeignKey(Archive, SET_NULL, null=True, blank=True)
    birth_date = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/img.png', blank=True, null=True)
    balance = IntegerField(default=0, blank=True)
    role = ManyToManyField('auth.Group', 'roles')
    branch = ManyToManyField('groups.Branch', 'branches')
    data = JSONField(null=True, blank=True)  # social account
    comment = TextField(blank=True, null=True)
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


class Lead(BaseModel):
    class LeadStatus(TextChoices):
        REQUESTS = 'requests', 'Requests'
        PENDING = 'pending', 'Pending'
        COLLECT = 'collect', 'Collect'

    full_name = CharField(max_length=255)
    comment = TextField()
    phone = IntegerField()
    status = CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.REQUESTS)
    lead_increment = ForeignKey('users.LeadIncrement', CASCADE)

    def __str__(self):
        return f'{self.full_name} | {self.phone}'


class LeadIncrement(BaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(UUIDBaseModel, BaseModel):
    title = CharField(max_length=255)
    text = RichTextUploadingField()
    public = BooleanField(default=False)
    created_by = ForeignKey('users.User', SET_NULL, 'created_by', null=True, blank=True)
    updated_by = ForeignKey('users.User', SET_NULL, 'updated_by', null=True, blank=True)
    visible_all = BooleanField(default=False, blank=True, null=True)
    view_count = IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
