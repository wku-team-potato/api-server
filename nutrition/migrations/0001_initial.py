# Generated by Django 4.2.16 on 2024-11-04 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foods',
            fields=[
                ('food_code', models.BigAutoField(primary_key=True, serialize=False)),
                ('food_name', models.CharField(max_length=20)),
                ('serving_size', models.CharField(help_text='g', max_length=20)),
                ('energy', models.FloatField(help_text='kcal')),
                ('carbohydrate', models.FloatField(help_text='g')),
                ('sugars', models.FloatField(help_text='g', null=True)),
                ('fat', models.FloatField(help_text='g', null=True)),
                ('protein', models.FloatField(help_text='g')),
                ('calcium', models.FloatField(help_text='mg', null=True)),
                ('phosphorus', models.FloatField(help_text='mg', null=True)),
                ('sodium', models.FloatField(help_text='mg', null=True)),
                ('potassium', models.FloatField(help_text='mg', null=True)),
                ('magnesium', models.FloatField(help_text='mg', null=True)),
                ('iron', models.FloatField(help_text='mg', null=True)),
                ('zinc', models.FloatField(help_text='mg', null=True)),
                ('cholesterol', models.FloatField(help_text='mg', null=True)),
                ('trans_fat', models.FloatField(help_text='g', null=True)),
            ],
            options={
                'verbose_name': 'Food Nutrition',
                'verbose_name_plural': 'Food Nutrition',
            },
        ),
    ]
