# Generated by Django 4.0.5 on 2022-06-15 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0005_sitereview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseimages',
            name='house_image',
            field=models.ImageField(default='default.jpg', upload_to='house_images/'),
        ),
    ]
