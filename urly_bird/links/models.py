from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.utils import timezone


class Bookmark(models.Model):
    url = models.URLField(max_length=255)
    code = models.CharField(max_length=255, unique=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.title)


#######################################################################################################################

class Click(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    bookmark = models.ForeignKey(Bookmark)
    timestamp = models.DateTimeField(default=timezone.now())

    # def to_dict(self):
    #     model_dict = {'user': self.user,
    #                   'bookmark': self.bookmark,
    #                   'timestamp': self.timestamp
    #                   }
    #     return model_dict

    def __str__(self):
        return str("{}: {}".format(self.user.id, self.timestamp))

#######################################################################################################################
from faker import Faker
import random

fake = Faker()

"""These functions create objects for development only, do not run"""


def make_users():
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
