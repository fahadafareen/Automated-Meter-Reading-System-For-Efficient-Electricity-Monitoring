from django.db import models



class registration(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150) 
    address = models.CharField(max_length=150) 
    location = models.CharField(max_length=150)
    
class consumerr(models.Model):
    name = models.CharField(max_length=150)
    meter_number = models.CharField(max_length=150)  




class bills(models.Model):
    consumerid = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    bill_amount = models.CharField(max_length=150) 
    due_date = models.CharField(max_length=150) 
    status = models.CharField(max_length=150)    
    cid = models.CharField(max_length=150)    

class news(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    post_date = models.CharField(max_length=150)
    is_alert = models.BooleanField(default=False)
    zone = models.CharField(max_length=150, default='All Zones')
    
    
class analyzing(models.Model):
    meternumber = models.CharField(max_length=150)
    currentreading = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    
class meter(models.Model):
    meternumber = models.CharField(max_length=150)
    status = models.CharField(max_length=150)   

class payment(models.Model):
    paymenttype = models.CharField(max_length=150)
    bill_amount = models.CharField(max_length=150)
    cardnum = models.CharField(max_length=150)
    ccvnum = models.CharField(max_length=150)
    expdate = models.CharField(max_length=150)
    status = models.CharField(max_length=150)     
    date = models.CharField(max_length=150)     
    uid = models.CharField(max_length=150)     
    cardname = models.CharField(max_length=150)

    
    
class complaints(models.Model):
    consumerid = models.CharField(max_length=150)
    complaintname = models.CharField(max_length=150)
    description = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    photoss = models.FileField(max_length=150)
    status = models.CharField(max_length=150)     
    cid = models.CharField(max_length=150)     

class chat(models.Model):
    sender = models.CharField(max_length=150)
    receiver = models.CharField(max_length=150)
    message = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class worker(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    email = models.CharField(max_length=150)
    password = models.CharField(max_length=150) 
    address = models.CharField(max_length=150) 
    location = models.CharField(max_length=150)
    role = models.CharField(max_length=150)

class Zone(models.Model):
    name = models.CharField(max_length=150)
    status = models.CharField(max_length=150) # Normal, Maintenance, Power Outage
    category = models.CharField(max_length=150) # e.g. Zone 1, Zone 2

class Dispatch(models.Model):
    workerid = models.CharField(max_length=150)
    zoneid = models.CharField(max_length=150)
    date = models.CharField(max_length=150)
    status = models.CharField(max_length=150)
    details = models.CharField(max_length=250, default='No details provided')

class MaintenanceReport(models.Model):
    workerid = models.CharField(max_length=150)
    zoneid = models.CharField(max_length=150)
    content = models.TextField(max_length=500)
    date = models.CharField(max_length=150)

class NewConnection(models.Model):
    uid = models.CharField(max_length=150)
    address = models.CharField(max_length=250)
    connection_type = models.CharField(max_length=150) 
    phase = models.CharField(max_length=150, default='1-Phase')
    status = models.CharField(max_length=150, default='Pending')
    date = models.CharField(max_length=150)

class SolarConnection(models.Model):
    uid = models.CharField(max_length=150)
    solar_capacity = models.CharField(max_length=150)
    status = models.CharField(max_length=150, default='Pending')
    date = models.CharField(max_length=150)

class NameChange(models.Model):
    uid = models.CharField(max_length=150)
    new_name = models.CharField(max_length=150)
    reason = models.CharField(max_length=150)
    status = models.CharField(max_length=150, default='Pending')
    date = models.CharField(max_length=150)

class TariffChange(models.Model):
    uid = models.CharField(max_length=150)
    current_plan = models.CharField(max_length=150)
    new_plan = models.CharField(max_length=150)
    status = models.CharField(max_length=150, default='Pending')
    date = models.CharField(max_length=150)

class energy_data(models.Model):
    uid = models.CharField(max_length=150)
    current = models.FloatField(default=0.0)
    power = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    date = models.DateTimeField(auto_now_add=True)

