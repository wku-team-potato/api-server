# Generated by Django 4.2.16 on 2024-11-05 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_item_table_alter_purchaserecord_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='img',
            field=models.ImageField(upload_to='media/images/items/'),
        ),
    ]
