# Generated by Django 3.2 on 2023-08-24 16:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.RegexValidator(message='В названии рецепта совсем нет букв', regex='.*[a-zA-Z].*')], verbose_name='Название блюда'),
        ),
    ]
