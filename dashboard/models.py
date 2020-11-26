from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True) #means a user can have only one customer and a customer can have only one user
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    usn = models.CharField(max_length=100,unique=True)
    phone = PhoneNumberField(unique=True)
    branch = models.CharField(max_length=100)
    year = models.IntegerField()
    gender = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name  #returning the string value,this is the value that comes in admin panel when we create model.

class Mentor(models.Model):
    mentor_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = PhoneNumberField(unique=True)
    experience = models.TextField(max_length=2000,null=True)
    img = models.ImageField(upload_to='mentor_imgs',null=True)
    sport = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.mentor_name

class Events(models.Model):
    event_name = models.CharField(max_length=100)
    event_description = models.TextField(max_length=500,null=True)
    img = models.ImageField(upload_to='events_imgs',null=True)
    date = models.DateField(default=now)
    place = models.CharField(max_length=100)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    deadline = models.DateField(default=now)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE,null=True,blank=True)
    
    class Meta:
        verbose_name_plural = "Events"

    def __str__(self):
        return self.event_name
    
class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True,blank=True)
    event = models.ForeignKey(Events, on_delete=models.CASCADE,null=True,blank=True)
    selected = models.BooleanField(default=False)

    def __str__(self):
        return self.student.name+"-"+self.student.usn+"-"+self.event.event_name

class Gallery(models.Model):
    img = models.ImageField(upload_to='gallery_imgs',null=True)
    img_description = models.TextField(max_length=500,null=True)

    class Meta:
        verbose_name_plural = "Gallery"

class Suggestions(models.Model):
    suggestion = models.TextField(max_length=500,null=True)
