# Generated by Django 4.2.16 on 2024-09-24 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutrition_api', '0004_alter_foods_serving_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foods',
            name='ash',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='beta_carotene',
            field=models.FloatField(help_text='μg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='calcium',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='carbohydrate',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='cholesterol',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='dietary_fiber',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='energy',
            field=models.FloatField(help_text='kcal', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='fat',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='iron',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='moisture',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='niacin',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='phosphorus',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='potassium',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='protein',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='retinol',
            field=models.FloatField(help_text='μg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='riboflavin',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='saturated_fat',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='sodium',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='sugars',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='thiamin',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='trans_fat',
            field=models.FloatField(help_text='g', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='vitamin_a',
            field=models.FloatField(help_text='μg RAE', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='vitamin_c',
            field=models.FloatField(help_text='mg', null=True),
        ),
        migrations.AlterField(
            model_name='foods',
            name='vitamin_d',
            field=models.FloatField(help_text='μg', null=True),
        ),
    ]
