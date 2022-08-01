from django.db import models

class Machine(models.Model):
    machine = models.CharField(max_length=10)

class Section(models.Model):
    section = models.CharField(max_length=50)
    roomNO = models.IntegerField()
    wing = models.CharField(max_length=35)

class Hardware(models.Model):
    machine_type = models.CharField(max_length=10)
    machine_no = models.CharField(max_length=35)
    U_id = models.CharField(max_length=35)
    specification = models.CharField(max_length=80)
    purchase_data = models.DateField()
    cost = models.IntegerField()
    stock_register = models.IntegerField()
    war_amc = models.CharField(max_length=15)
    warenty  = models.IntegerField()

class Entry(models.Model):
    machine_id = models.CharField(max_length=35)
    sec_emp = models.CharField(max_length=3)
    section_name = models.CharField(max_length=50)
    employee_name = models.CharField(max_length=30)
    employee_id = models.CharField(max_length=35)
    issue_date = models.DateField()
    username = models.CharField(max_length=30)
    wing = models.CharField(max_length=35)
    status = models.BooleanField(default=False)

class Wing(models.Model):
    wing = models.CharField(max_length=35)
# Create your models here.
