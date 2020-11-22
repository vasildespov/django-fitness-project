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
from django.db.models.fields import SlugField
from django.utils.timezone import now
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.urls import reverse


class Article(Model):
    author = ForeignKey(User, on_delete=CASCADE)
    title = CharField(max_length=30, unique=True, blank=False)
    subtitle = CharField(max_length=100, blank=False)
    category = CharField(max_length=20, blank=False)
    # content = TextField(blank=False)
    slug = SlugField(max_length=100, default="")
    content = RichTextField(blank=True, null=True)
    date = DateTimeField(default=now)
    cover = ImageField(
        upload_to="article-covers", null=True, default="cover-default.jpg"
    )

    def __str__(self) -> str:
        return self.title

    def datepublished(self):
        return self.date.strftime("%B %d, %Y")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("article detail", kwargs={"pk": self.pk, "slug": self.slug})


class Profile(Model):
    user = OneToOneField(User, on_delete=CASCADE, unique=True, primary_key=True)
    profile_pic = ImageField(upload_to="profile_pics", default="default.png")

    def __str__(self) -> str:
        return f"{self.user.username} Profile"


class Like(Model):
    user = ForeignKey(User, on_delete=CASCADE)
    article = ForeignKey(Article, on_delete=CASCADE)

    def __str__(self) -> str:
        return f"{self.user.username} likes {self.article.title}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()