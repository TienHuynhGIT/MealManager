# Generated by Django 3.1.5 on 2021-01-09 16:12

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Bild')),
            ],
        ),
        migrations.CreateModel(
            name='Weekday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Avatar')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Bild')),
                ('difficulty', models.SmallIntegerField(blank=True, choices=[(1, 'einfach'), (2, 'mittel'), (3, 'schwer')], null=True, verbose_name='Schwierigkeitsgrad')),
                ('duration', models.CharField(blank=True, max_length=200, null=True, verbose_name='Zubereitungszeit')),
                ('portion_size', models.PositiveIntegerField(blank=True, null=True, verbose_name='Portion(en)')),
                ('ingredients', models.TextField(blank=True, null=True, verbose_name='Zutat(en)')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Beschreibung')),
                ('created_at', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='Erstell-/Updatedatum')),
                ('author', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor')),
                ('weekdays', models.ManyToManyField(blank=True, null=True, to='gallery.Weekday', verbose_name='Wochentag(e)')),
            ],
        ),
    ]
