# Generated by Django 3.2.6 on 2022-04-07 11:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_shoppingcart_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_favorites', to='recipes.recipe', verbose_name='Избранные у пользователей'),
        ),
    ]
