# Generated by Django 2.2.10 on 2020-03-03 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultants', '0009_auto_20200222_0344'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultant',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
