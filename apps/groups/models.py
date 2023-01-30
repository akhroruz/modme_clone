from django.db.models import IntegerField, CharField, Model, ImageField, TextField, ForeignKey, SET_NULL, TextChoices, \
    TimeField, DecimalField, DateField, BooleanField, CASCADE

from apps.shared.models import BaseModel


class Role(BaseModel):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Branch(BaseModel):
    name = CharField(max_length=255)
    address = CharField(max_length=255)
    phone = IntegerField(unique=True)
    about = TextField()
    image = ImageField(max_length=100, upload_to='images/')

    def __str__(self):
        return self.name


class Room(BaseModel):
    name = CharField(max_length=255)
    branch = ForeignKey('groups.Branch', CASCADE)


class Course(BaseModel):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)


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

    name = CharField(max_length=255)
    days = CharField(max_length=50, choices=DaysChoice.choices)  # dars bo'lis kunlari
    room = ForeignKey('groups.Room', SET_NULL, null=True)
    teacher = ForeignKey('users.User', SET_NULL, null=True, related_name='teachers')
    start_time = TimeField(null=True, blank=True)  # dars boshlanish vaqti
    group_time = DateField(null=True, blank=True)  # guruh ochilish sanasi

