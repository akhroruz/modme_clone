from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, JSONField, \
    TextField, DateTimeField, ManyToManyField, ForeignKey, CASCADE, BooleanField, SET_NULL, BigIntegerField, \
    PositiveIntegerField

from shared.models import BaseModel
from users.managers import MyUserManager


class Archive(BaseModel):
    name = CharField(max_length=100)
    company = ForeignKey('groups.Company', CASCADE)

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    email = None
    username = None
    groups = None

    phone = CharField(max_length=15, unique=True)
    is_archive = BooleanField(default=False)
    archive = ForeignKey(Archive, SET_NULL, null=True, blank=True)
    birth_date = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/img.png', blank=True, null=True)
    balance = IntegerField(default=0, blank=True)
    role = ManyToManyField('auth.Group')
    branch = ManyToManyField('groups.Branch')
    data = JSONField(null=True, blank=True)  # social account
    deleted_at = DateTimeField(null=True)
    comment = GenericRelation('users.Comment')

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
    content_type = ForeignKey('contenttypes.ContentType', CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()
    creater = ForeignKey('users.User', SET_NULL, null=True)


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


class Blog(BaseModel):
    title = CharField(max_length=255)
    text = RichTextUploadingField()
    public = BooleanField(default=False)
    created_by = ForeignKey('users.User', SET_NULL, 'created_by', null=True, blank=True)
    updated_by = ForeignKey('users.User', SET_NULL, 'updated_by', null=True, blank=True)
    visible_all = BooleanField(default=False, blank=True, null=True)
    view_count = BigIntegerField(default=0, blank=True, null=True)
    company = ForeignKey('groups.Company', CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)
