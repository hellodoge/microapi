from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.http import urlsafe_base64_encode
from picklefield.fields import PickledObjectField
from os import urandom


def random_uid():
    while True:
        guess = urlsafe_base64_encode(urandom(9))
        if not API.objects.filter(uid=guess).exists():
            return guess


class API(models.Model):
    class RequestBodyType(models.TextChoices):
        RAW_TEXT = 'R', _('Raw text')
        RAW_BIN = 'B', _('Raw binary')
        JSON = 'J', _('JSON')

    uid = models.CharField(
        primary_key=True,
        max_length=12,
        unique=True,
        default=random_uid
    )
    title = models.CharField(max_length=100)
    python_code = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    request_body_type = models.CharField(
        max_length=1,
        choices=RequestBodyType.choices,
        default=RequestBodyType.JSON
    )
    enabled = models.BooleanField(default=True)
    modify_date = models.DateTimeField(auto_now=True)
    storage = PickledObjectField(null=True)
    compiles = models.BooleanField(null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('api-make-request', args=[self.uid])
