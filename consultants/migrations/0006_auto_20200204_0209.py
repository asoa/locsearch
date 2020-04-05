# Generated by Django 2.2.9 on 2020-02-04 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultants', '0005_auto_20200201_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultant',
            name='is_ambassador',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='is_distributor',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='is_r_certified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='is_trainee',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='consultant',
            name='is_trichology',
            field=models.BooleanField(default=False),
        ),
    ]
