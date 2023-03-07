from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models import TextChoices, CharField, IntegerField, DateField, ImageField, JSONField, \
    TextField, DateTimeField, ManyToManyField, ForeignKey, CASCADE, BooleanField, SET_NULL, BigIntegerField, \
    PositiveIntegerField, Model, FileField

from shared.models import BaseModel
from users.managers import MyUserManager


class ArchivedUser(BaseModel):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    class UserTypeChoice(TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'

    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    phone = CharField(max_length=15, unique=True)
    birth_date = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/img.png', blank=True, null=True)
    balance = IntegerField(default=0, blank=True)
    role = ManyToManyField('auth.Group')
    branch = ManyToManyField('groups.Branch')
    data = JSONField(null=True, blank=True)  # social account
    deleted_at = DateTimeField(auto_now=True)
    destroyer = ForeignKey('users.User', SET_NULL, null=True)
    comment = GenericRelation('users.Comment')
    user_type = CharField(max_length=10, choices=UserTypeChoice.choices, blank=True, null=True)
    archive_reason = ForeignKey('groups.ArchiveReason', SET_NULL, null=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'{self.phone}'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class User(AbstractUser, BaseModel):
    class GenderChoose(TextChoices):
        MALE = 'male', 'Male'
        FEMALE = 'female', 'Female'

    class UserTypeChoice(TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'

    email = None
    username = None
    groups = None

    phone = CharField(max_length=15, unique=True)
    birth_date = DateField(blank=True, null=True)
    gender = CharField(max_length=25, choices=GenderChoose.choices, blank=True, null=True)
    photo = ImageField(max_length=100, upload_to='profiles/', default='media/img.png', blank=True, null=True)
    balance = IntegerField(default=0, blank=True)
    role = ManyToManyField('auth.Group')
    branch = ManyToManyField('groups.Branch', 'branches')
    data = JSONField(null=True, blank=True)
    comment = GenericRelation('users.Comment')
    user_type = CharField(max_length=10, choices=UserTypeChoice.choices, blank=True, null=True)

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

    @property
    def number_of_groups(self):
        return self.groups.count()

    @property
    def roles(self):
        return self.role.values('id', 'name')

    @property
    def company_id(self):
        return self.branch.first().company_id

    @property
    def branches(self):
        return self.branch.values('id', 'name')


class Comment(BaseModel):
    text = TextField()
    content_type = ForeignKey('contenttypes.ContentType', CASCADE)
    object_id = PositiveIntegerField()
    content_object = GenericForeignKey()
    author = ForeignKey('users.User', SET_NULL, null=True)


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
    public = BooleanField(default=False)  # TODO
    created_by = ForeignKey('users.User', SET_NULL, 'created_by', null=True, blank=True)
    updated_by = ForeignKey('users.User', SET_NULL, 'updated_by', null=True, blank=True)
    visible_all = BooleanField(default=False, blank=True, null=True)  # TODO
    view_count = BigIntegerField(default=0, blank=True, null=True)
    company = ForeignKey('groups.Company', CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)


class ExcelFile(Model):  # TODO
    file = FileField(upload_to='excel')
