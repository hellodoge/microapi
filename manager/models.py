from django.db import models
from api.models import API


class APILog(models.Model):
    message = models.CharField(max_length=100)
    time_logged = models.DateTimeField(auto_now=True)
    api = models.ForeignKey(API, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.api.owner} ({self.api}) {self.time_logged.strftime("%Y-%m-%d %H:%M:%S")}'
