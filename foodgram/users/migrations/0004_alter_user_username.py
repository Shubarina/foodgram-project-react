# Generated by Django 3.2 on 2023-07-20 17:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20230720_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+\\Z')], verbose_name='Логин'),
        ),
    ]
