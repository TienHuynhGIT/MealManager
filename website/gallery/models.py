from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField('Avatar', upload_to="avatars", blank=True, null=True) 



def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Weekday(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    DIFFICULTY_EASY = 1
    DIFFICULTY_MEDIUM = 2
    DIFFICULTY_HARD = 3

    DIFFICULTIES = (
        (DIFFICULTY_EASY, 'einfach'),
        (DIFFICULTY_MEDIUM, 'mittel'),
        (DIFFICULTY_HARD, 'schwer'),
    )

    name = models.CharField(max_length=200, verbose_name='Name')
    image = models.ImageField(upload_to="", blank=True, null=True, verbose_name='Bild')
    difficulty = models.SmallIntegerField(choices=DIFFICULTIES, blank=True, null=True, verbose_name='Schwierigkeitsgrad')
    duration = models.CharField(max_length=200, blank=True, null=True, verbose_name='Zubereitungszeit')
    portion_size = models.PositiveIntegerField(blank=True, null=True, verbose_name='Portion(en)')
    ingredients = models.TextField(blank=True, null=True, verbose_name='Zutat(en)')
    description = models.TextField(blank=True, null=True, verbose_name='Beschreibung')
    weekdays = models.ManyToManyField(Weekday, blank=True, null=True, verbose_name='Wochentag(e)')
    published = models.BooleanField(default=False, verbose_name="Veröffentlichen")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=User,
        null=True,
        verbose_name='Autor',
    )
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True, verbose_name='Erstell-/Updatedatum')
    
    def __str__(self):
        return self.name


class Entry(models.Model):
    weekday = models.ForeignKey(Weekday, on_delete=models.CASCADE)
    recepi = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)







