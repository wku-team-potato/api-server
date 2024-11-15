# Generated by Django 4.2.16 on 2024-11-16 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profile', '0003_profile_consecutive_attendance_days_and_more'),
        ('meal', '0004_usermeal_serving_size_alter_usermeal_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_time', models.CharField(choices=[('breakfast', '아침'), ('lunch', '점심'), ('dinner', '저녁')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profile.profile')),
            ],
            options={
                'db_table': 'meal',
            },
        ),
    ]