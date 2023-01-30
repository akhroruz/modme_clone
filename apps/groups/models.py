from django.contrib.postgres.fields import ArrayField
from django.db.models import IntegerField, CharField, Model, ImageField, TextField, ForeignKey, SET_NULL, TextChoices, \
    TimeField, DecimalField, DateField, BooleanField, CASCADE, ManyToManyField

from apps.shared.models import BaseModel


class Role(BaseModel):
    name = CharField(max_length=255)
    user = ManyToManyField('users.User')

    def __str__(self):
        return self.name


class Branch(BaseModel):
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    phone = IntegerField(unique=True)
    about = TextField()
    image = ImageField(max_length=100, upload_to='images/')
    ceo = ManyToManyField('users.User', related_name='branch_ceo')

    def __str__(self):
        return self.name


class Room(BaseModel):
    name = CharField(max_length=255)
    branch = ForeignKey(to='groups.Branch', on_delete=CASCADE)


class Course(BaseModel):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    branch = ForeignKey('groups.Branch', SET_NULL, null=True)
    group = ForeignKey('groups.Group', SET_NULL, null=True, related_name='course_group')


class Holiday(BaseModel):  # dam olish kunlari
    name = CharField(max_length=255)
    holiday_date = DateField(null=True, blank=True)
    affect_payment = BooleanField(default=False)  # to'lovga tasir qilishi
    branch = ForeignKey('groups.Branch', CASCADE)


class Group(BaseModel):
    class DaysChoice(TextChoices):
        ODD_DAYS = 'odd_days', 'Odd days'
        EVEN_DAYS = 'even days', 'Even Days'
        DAY_OFF = 'day_off', 'Day off'

    class StatusChoice(TextChoices):
        ARCHIVED = 'is_archived', 'Is Archived'  # arxivlangan gurux lar
        COMPLETED = 'is_completed', 'Is Completed'  # yakunlangan gurux lar
        ACTIVE = 'is_active', 'Is Active'  # faol gurux lar

    name = CharField(max_length=255)
    days = CharField(max_length=50, choices=DaysChoice.choices)  # dars bo'lis kunlari
    status = CharField(max_length=25, choices=StatusChoice.choices, default=StatusChoice.ACTIVE)
    room = ForeignKey('groups.Room', SET_NULL, null=True, related_name='group_room')
    teacher = ForeignKey('users.User', SET_NULL, null=True, related_name='teacher')
    start_time = TimeField(null=True, blank=True)  # dars boshlanish vaqti
    end_time = TimeField(null=True, blank=True)
    course = ForeignKey('groups.Course', SET_NULL, null=True, related_name='group_course')
    branch = ForeignKey('groups.Branch', CASCADE, related_name='group_branch')
    start_date = DateField(null=True, blank=True)
    end_date = DateField(null=True, blank=True)
    tags = ArrayField(CharField(max_length=255))
    comment = TextField(null=True, blank=True)

    @property
    def get_students(self):
        return self.user_set.all()

    @property
    def students_count(self):
        return self.user_set.count()

    @property
    def get_course(self):
        return self.course_set.all()
