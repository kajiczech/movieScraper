from django.db import models
from libs.models import BaseModel


# There can be distinctive movies or actors with the same names!
class Actor(BaseModel):
    name = models.CharField(max_length=255, null=False)
    # For SQLite database, we need to add this field for unicode search,
    unicode_name = models.CharField(max_length=255, null=False, help_text='Unaccented lowercase string for searching')
    date_of_birth = models.DateField(null=True)
    city_of_birth = models.CharField(max_length=255, null=True)

    class Meta:
        unique_together = ('name', 'unicode_name', 'date_of_birth', 'city_of_birth')


class Movie(BaseModel):
    name = models.CharField(max_length=255, null=False)
    year = models.IntegerField(null=False)
    unicode_name = models.CharField(max_length=255, null=False, help_text='Unaccented lowercase string for searching')
    actors = models.ManyToManyField(to=Actor, related_name='movies')

    class Meta:
        unique_together = ('name', 'unicode_name', 'year')

