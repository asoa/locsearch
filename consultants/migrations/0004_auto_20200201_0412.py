# Generated by Django 2.2.9 on 2020-02-01 04:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultants', '0003_consultant_zipcode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='consultant',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='consultant',
            name='last_name',
        ),
    ]