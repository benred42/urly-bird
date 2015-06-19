from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone


class Bookmark(models.Model):
    url = models.URLField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.title)


#######################################################################################################################

class Click(models.Model):
    user = models.ForeignKey(User)
    bookmark = models.ForeignKey(Bookmark)
    timestamp = models.DateTimeField()

    def __str__(self):
        return str("{}: {}".format(self.user.id, self.timestamp))

#######################################################################################################################
from faker import Faker
import random

fake = Faker()


def make_users():
    """Creates user objects for development only, do not run"""
    for index in range(100):
        user_name = fake.user_name()
        User.objects.create_user(username=user_name,
                                 email=(user_name + '@' + fake.free_email_domain()),
                                 password="batman")


def make_bookmarks():
    for user in User.objects.all():
        for _ in range(random.randint(10, 20)):
            bookmark = Bookmark(url=fake.url(),
                                code=fake.password(length=10, special_chars=False, digits=True, upper_case=True,
                                                   lower_case=True),
                                title=fake.color_name(),
                                description=fake.paragraph(nb_sentences=3, variable_nb_sentences=True),
                                timestamp=timezone.now(),
                                user=user,
                                )
            bookmark.save()


def make_clicks():
    for bookmark in Bookmark.objects.all():
        for index in range(random.randint(0, 1000)):
            click = Click(user=random.choice(User.objects.all()),
                          bookmark=bookmark,
                          timestamp=fake.date_time_between(start_date="-1y", end_date="now"),
                          )

            click.save()
