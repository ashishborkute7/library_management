from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta

# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name) + " ["+str(self.subject)+']'

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    classroom = models.CharField(max_length=10)
    branch = models.CharField(max_length=10)
    roll_no = models.CharField(max_length=15, blank=True)
    phone = models.CharField(max_length=10, blank=True)


    def __str__(self):
        return str(self.user) + " ["+str(self.branch)+']' + " ["+str(self.classroom)+']' + " ["+str(self.roll_no)+']'

def expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    student_id = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=15)
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)