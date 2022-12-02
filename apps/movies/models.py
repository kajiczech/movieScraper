from django.db import models
from libs.models import BaseModel


# There can be distinctive movies or actors with the same names!
class Actor(BaseModel):
    name = models.CharField(max_length=255, null=False)
    # For SQLite database, we need to add this field for unicode search,
    unicode_name = models.CharField(max_length=255, null=False, help_text='Unaccented lowercase word for searching')


class Movie(BaseModel):
    name = models.CharField(max_length=255, null=False)
    unicode_name = models.CharField(max_length=255, null=False, help_text='Unaccented lowercase word for searching')
    actors = models.ManyToManyField(to=Actor, related_name='movies')

