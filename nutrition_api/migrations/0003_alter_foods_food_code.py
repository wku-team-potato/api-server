# Generated by Django 4.2.16 on 2024-09-24 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition_api', '0002_alter_foods_food_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foods',
            name='food_code',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
