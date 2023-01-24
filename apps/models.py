from django.contrib.auth.models import AbstractUser
from django.db.models import IntegerField, CharField, Model, ImageField, TextField
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from shared.models import BaseModel


class Role(BaseModel):
    name = CharField(max_length=255)


class Branch(TranslatableModel, BaseModel):
    translations = TranslatedFields(
        address=CharField(_('address'), max_length=255),
        about=TextField(_('about'))
    )

    name = CharField(max_length=255)
    phone_number = IntegerField(unique=True)
    image = ImageField(upload_to='images/')
