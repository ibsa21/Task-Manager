# Generated by Django 4.0.3 on 2022-04-10 09:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_groupproject_members_groupproject_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupproject',
            name='deadline_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
