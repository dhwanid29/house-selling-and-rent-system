# Generated by Django 4.0.5 on 2022-06-14 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='amenities',
        ),
        migrations.AddField(
            model_name='house',
            name='amenities',
            field=models.ManyToManyField(to='house.amenities'),
        ),
    ]
