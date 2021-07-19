import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError


def validate_phone_number(value):
    number = re.search(r'^09\d{9}$', value)
    if number is None:
        raise ValidationError(
            _('%(value)s is not an acceptable phone number'),
            params={'value': value},
        )


class CustomUser(AbstractUser):
    phone_number = models.CharField(_('Phone Number'), validators=[validate_phone_number],
                                    max_length=11, unique=True, blank=False, default='')

    REQUIRED_FIELDS = ['phone_number', 'email']

    objects = CustomUserManager()
