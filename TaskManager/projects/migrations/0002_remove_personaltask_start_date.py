# Generated by Django 4.0.3 on 2022-04-06 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personaltask',
            name='start_date',
        ),
    ]