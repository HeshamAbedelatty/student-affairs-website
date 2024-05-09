from django.db import models

# Create your models here.


class studentdataa(models.Model):
    id = models.CharField(max_length=8,unique=True,null=False,primary_key=True)
    nationalnum = models.CharField(max_length=14,null=False,unique=True)
    name= models.CharField(max_length=50,null=False)
    dateofbirth=models.DateField()
    phone=models.CharField(max_length=15,null=False,unique=True)
    email=models.CharField(max_length=30,null=False,unique=True)
    gpa=models.DecimalField(max_digits=3,decimal_places=2)
    level=models.CharField(max_length=2,null=False)
    department=models.CharField(max_length=3)
    status=models.CharField(max_length=10,null=False)
    gender=models.CharField(max_length=15,null=False)
    class Meta:
        db_table = "StudentsData"
    def __str__(self):
        return self.name
    

class studentaffairsadmin(models.Model):
    nationalnum = models.CharField(max_length=14,null=False,unique=True,primary_key=True)
    name= models.CharField(max_length=50,null=False)
    dateofbirth=models.DateField()
    phone=models.CharField(max_length=15,null=False,unique=True)
    email=models.CharField(max_length=30,null=False,unique=True)
    username=models.CharField(max_length=30,null=False,unique=True)
    password=models.CharField(max_length=40,null=False)
    class Meta:
        db_table = "AdminsData"
    def __str__(self):
        return self.name

class activeuser(models.Model):
    status=models.CharField(max_length=50)
    username=models.CharField(max_length=30,unique=True)
    class Meta:
        db_table = "ActiveUser"
    def __str__(self):
        return self.username