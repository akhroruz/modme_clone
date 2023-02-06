from django.contrib.auth.models import Group as Gr, Group
from django.contrib.postgres.fields import ArrayField
from django.db.models import IntegerField, CharField, ImageField, TextField, ForeignKey, SET_NULL, TextChoices, \
    TimeField, DecimalField, DateField, BooleanField, CASCADE, ManyToManyField

from shared.models import BaseModel


class Company(BaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Branch(BaseModel):
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    company = ForeignKey('groups.Company', CASCADE)
    phone = CharField(max_length=10, unique=True)
    about = TextField(null=True, blank=True)
    image = ImageField(max_length=100, upload_to='images/', default='media/img.png')

    def __str__(self):
        return self.name


class Room(BaseModel):
    name = CharField(max_length=255)
    branch = ForeignKey('groups.Branch', CASCADE)

    def __str__(self):
        return self.name


class Course(BaseModel):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField(null=True, blank=True)
    image = ImageField(upload_to='courses/', null=True, blank=True)
    lesson_duration = IntegerField()
    course_duration = IntegerField()
    branch = ManyToManyField('groups.Branch')

    def __str__(self):
        return self.name


class Holiday(BaseModel):  # dam olish kunlari
    name = CharField(max_length=255)
    holiday_date = DateField(null=True, blank=True)
    affect_payment = BooleanField(default=False)  # to'lovga tasir qilishi
    branch = ForeignKey('groups.Branch', CASCADE)

    def __str__(self):
        return self.name


class CourseGroup(BaseModel):
    class DaysChoice(TextChoices):
        ODD_DAYS = 'odd_days', 'Odd days'
        EVEN_DAYS = 'even days', 'Even Days'
        DAY_OFF = 'day_off', 'Day off'

    class StatusChoice(TextChoices):
        ARCHIVED = 'is_archived', 'Is Archived'  # arxivlangan gurux lar
        COMPLETED = 'is_completed', 'Is Completed'  # yakunlangan gurux lar
        ACTIVE = 'is_active', 'Is Active'  # faol gurux lar

    name = CharField(max_length=255)
    days = CharField(max_length=50, choices=DaysChoice.choices)  # dars bo'lish kunlari
    status = CharField(max_length=25, choices=StatusChoice.choices, default=StatusChoice.ACTIVE)
    room = ManyToManyField('groups.Room', 'group_room')
    students = ManyToManyField('users.User')
    teachers = ManyToManyField('users.User', 'teachers')
    start_time = TimeField(null=True, blank=True)  # dars boshlanish vaqti
    end_time = TimeField(null=True, blank=True)
    course = ForeignKey('groups.Course', SET_NULL, null=True, related_name='group_course')
    branch = ManyToManyField('groups.Branch')
    start_date = DateField(null=True, blank=True)
    end_date = DateField(null=True, blank=True)
    tags = ArrayField(CharField(max_length=255))
    comment = TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_students(self):
        return self.students.all()

    @property
    def students_count(self):
        return self.students.count()

    class Meta:
        unique_together = ('course', 'name')


class Lesson(BaseModel):
    title = CharField(max_length=255)
    course = ForeignKey('groups.Course', SET_NULL, null=True)
    group = ForeignKey('groups.CourseGroup', SET_NULL, null=True)
