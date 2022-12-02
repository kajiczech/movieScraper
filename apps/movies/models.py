from django.db import models
from libs.models import BaseModel


# There can be distinctive movies or actors with the same names!
class Actor(BaseModel):
    name = models.CharField(max_length=255, null=False)


class Movie(BaseModel):
    name = models.CharField(max_length=255, null=False)
    actors = models.ManyToManyField(to=Actor, related_name='movies')

