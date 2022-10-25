from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    level = models.CharField(max_length=50)
    skills = models.CharField(max_length=256)
    language = models.CharField(max_length=50)

    class Meta:
        db_table = 'user'
        verbose_name = "User Info Table"


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=256)
    university_name = models.CharField(max_length=256)
    course_language = models.CharField(max_length=256)
    course_rating = models.FloatField()
    course_level = models.CharField(max_length=256)
    course_detail = models.TextField()
    course_skills = models.CharField(max_length=256)
    course_link = models.URLField(default="https://www.coursera.org/")
    course_image = models.URLField(default="https://is4-ssl.mzstatic.com/image/thumb/Purple122/v4/26/af/93/26af935f-f1bf-0c1d-22ac-fdf72bdc3609/AppIcon-0-1x_U007emarketing-0-7-0-0-85-220-0.png/1200x630wa.png")
    reco_course_id = models.JSONField()

    class Meta:
        db_table = 'course'
        verbose_name = "Course Info Table"
