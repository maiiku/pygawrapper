from django.db import models

# Create your models here.

class Pygawrapper(models.Model):
    user_id = models.PositiveIntegerField(unique=True)
    utma = models.TextField(default=None, null=True, editable=False)
    utmb = models.TextField(default=None, null=True, editable=False)

