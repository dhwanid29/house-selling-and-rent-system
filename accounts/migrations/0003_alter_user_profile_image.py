# Generated by Django 4.0.5 on 2022-06-09 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(default='default.jpg', upload_to='uploads/'),
        ),
    ]
