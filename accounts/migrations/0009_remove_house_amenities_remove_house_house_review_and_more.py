# Generated by Django 4.0.5 on 2022-06-14 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_amenities_house_housereview_alter_user_profile_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='amenities',
        ),
        migrations.RemoveField(
            model_name='house',
            name='house_review',
        ),
        migrations.RemoveField(
            model_name='house',
            name='user',
        ),
        migrations.RemoveField(
            model_name='houseimages',
            name='house',
        ),
        migrations.DeleteModel(
            name='Amenities',
        ),
        migrations.DeleteModel(
            name='House',
        ),
        migrations.DeleteModel(
            name='HouseImages',
        ),
        migrations.DeleteModel(
            name='HouseReview',
        ),
    ]
