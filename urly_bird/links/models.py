from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bookmark(models.Model):
    url = models.URLField(max_length=255)
    code = models.CharField(max_length=255)
    tile = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.title)

#######################################################################################################################

class Click(models.Model):
    user = models.ForeignKey(User)
    bookmark = models.ForeignKey(Bookmark)
    timestamp = models.DateTimeField()
