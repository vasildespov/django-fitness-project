from django.contrib.auth.models import User
from django.db.models import (
    CharField,
    DateTimeField,
    ImageField,
    Model,
)
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey, ManyToManyField, OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from ckeditor.fields import RichTextField


class Article(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=30, unique=True, blank=False)
    subtitle = CharField(max_length=100, blank=False)
    category = CharField(max_length=20, blank=False)
    # content = TextField(blank=False)
    content = RichTextField(blank=True, null=True)
    date = DateTimeField(default=now)

    def __str__(self) -> str:
        return self.title


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, unique=True, primary_key=True)
    profile_pic = ImageField(upload_to="profile_pics", default="default.png")
    saved_articles = ManyToManyField(Article, related_name="saved_articles", blank=True)
    created_articles = ManyToManyField(Article, related_name="created_articles", blank=True)

    def __str__(self) -> str:
        return f"{self.user.username} Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()