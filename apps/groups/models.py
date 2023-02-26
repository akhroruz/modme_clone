from django.contrib.postgres.fields import ArrayField
from django.db.models import IntegerField, CharField, ImageField, TextField, ForeignKey, SET_NULL, TextChoices, \
    TimeField, DecimalField, DateField, BooleanField, CASCADE, ManyToManyField

from shared.models import BaseModel


class Company(BaseModel):  # checked
    name = CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'


class Branch(BaseModel):  # checked
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    company = ForeignKey('groups.Company', CASCADE)
    phone = CharField(max_length=10, unique=True)
    about = TextField(null=True, blank=True)
    image = ImageField(max_length=100, upload_to='images/', default='media/img.png')

    class Meta:
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name


class Room(BaseModel):  # checked
    name = CharField(max_length=255)
    branch = ForeignKey('groups.Branch', CASCADE)

    def __str__(self):
        return self.name


class Course(BaseModel):  # checked
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField(null=True, blank=True)
    image = ImageField(upload_to='courses/', null=True, blank=True)
    lesson_duration = IntegerField()
    course_duration = IntegerField()
    company = ForeignKey('groups.Company', CASCADE)

    def __str__(self):
        return self.name


class Holiday(BaseModel):  # noqa| dam olish kunlari
    name = CharField(max_length=255)
    holiday_date = DateField(null=True, blank=True)
    affect_payment = BooleanField(default=False)  # noqa| to'lovga tasir qilishi
    branch = ForeignKey('groups.Branch', CASCADE)

    def __str__(self):
        return self.name


class Group(BaseModel):  # checked
    class DaysChoice(TextChoices):
        ODD_DAYS = 'odd_days', 'Odd days'
        EVEN_DAYS = 'even days', 'Even Days'
        DAY_OFF = 'day_off', 'Day off'

    class StatusChoice(TextChoices):
        ARCHIVED = 'is_archived', 'Is Archived'  # noqa| arxivlangan gurux lar
        COMPLETED = 'is_completed', 'Is Completed'  # noqa| yakunlangan gurux lar
        ACTIVE = 'is_active', 'Is Active'  # noqa| faol gurux lar

    name = CharField(max_length=255)
    days = CharField(max_length=50, choices=DaysChoice.choices)  # noqa| dars bo'lish kunlari
    status = CharField(max_length=25, choices=StatusChoice.choices, default=StatusChoice.ACTIVE)
    room = ForeignKey('groups.Room', CASCADE, 'groups')
    students = ManyToManyField('users.User')
    teacher = ForeignKey('users.User', SET_NULL, 'groups', null=True, blank=True)
    start_time = TimeField(null=True, blank=True)  # noqa| dars boshlanish vaqti
    end_time = TimeField(null=True, blank=True)
    course = ForeignKey('groups.Course', SET_NULL, 'groups', null=True)
    branch = ForeignKey('groups.Branch', CASCADE, 'groups')
    start_date = DateField(null=True, blank=True)
    end_date = DateField(null=True, blank=True)
    tags = ArrayField(CharField(max_length=255))
    # comment = GenericRelation('users.Comment')

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
    group = ForeignKey('groups.Group', SET_NULL, null=True)
