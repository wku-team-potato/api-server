# Generated by Django 4.2.16 on 2024-09-24 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foods',
            name='food_code',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]