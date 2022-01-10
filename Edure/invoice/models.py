from django.db import models
from django.db.models.base import Model

# Create your models here.
class Admins(models.Model):
    name=models.CharField(max_length=200,default='')
    Password=models.CharField(max_length=20,default='')
    Std_Type=models.CharField(max_length=100,default='')

    def __str__(self):
        return self.Std_Type


class Stud_reg(models.Model):
    Stud_IDD=models.CharField(max_length=300,default='')
    Stud_name=models.CharField(max_length=300,default='')
    Stud_mail=models.CharField(max_length=300,default='')
    Stud_course=models.CharField(max_length=300,default='')
    Stud_number=models.CharField(max_length=300,default='')
    Stud_paid=models.CharField(max_length=1000,default='')
    Stud_balance=models.CharField(max_length=1000,default='')
    Stud_address=models.CharField(max_length=500,default='')
    Stud_image=models.ImageField(upload_to='Stud_image',null=True,blank=True)   
    Course_amount=models.CharField(max_length=1000,default='')
    Join_date=models.CharField(max_length=300,default='')
    End_date=models.CharField(max_length=300,default='')
    def __str__(self):
        return self.Stud_name     


