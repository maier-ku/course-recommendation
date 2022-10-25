# Generated by Django 4.1.2 on 2022-10-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='skills',
            new_name='course_skills',
        ),
        migrations.AddField(
            model_name='course',
            name='course_image',
            field=models.URLField(default='https://is4-ssl.mzstatic.com/image/thumb/Purple122/v4/26/af/93/26af935f-f1bf-0c1d-22ac-fdf72bdc3609/AppIcon-0-1x_U007emarketing-0-7-0-0-85-220-0.png/1200x630wa.png'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_link',
            field=models.URLField(default='https://www.coursera.org/'),
        ),
    ]
