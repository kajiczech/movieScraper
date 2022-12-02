import uuid
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    date_created = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        abstract = True
