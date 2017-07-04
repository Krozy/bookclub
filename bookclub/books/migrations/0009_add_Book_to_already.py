# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-21 14:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import uuid
from django.db import migrations, transaction
from django.apps import apps


def forward(apps, _):
    Book = apps.get_model('books', 'Book')
    BooksAlreadyRead = apps.get_model('books', 'BooksAlreadyRead')

    for row in Book.objects.all():
        ar = BooksAlreadyRead()
        ar.user = row.user_name
        ar.book = row
        ar.read_at = row.data_read
        ar.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0008_rename_booker'),
    ]

    operations = [
        migrations.RunPython(forward),
    ]