# Generated by Django 5.0.6 on 2024-07-20 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0002_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='Profile'),
        ),
    ]
