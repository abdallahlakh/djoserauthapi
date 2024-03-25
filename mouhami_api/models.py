from django.db import models
from django.utils import timezone

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=255, unique=True,primary_key=True)
    
class Specialities(models.Model):
    name = models.CharField(max_length=255, unique=True,primary_key=True)

class Review(models.Model):
    customer = models.ForeignKey('account.User', on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.TextField()
    lawyer = models.ForeignKey('Lawyer', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)

    def customer_name(self):
        return self.customer.name
class Lawyer(models.Model):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    photo = models.CharField(max_length=255,null=True, blank=True)
    location = models.CharField(max_length=255)
    lng = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    specialities = models.ManyToManyField('Specialities', blank=True)
    rating = models.FloatField(null=True, blank=True)
    languages = models.ManyToManyField('Language', blank=True)


class Customer(models.Model):
    user = models.OneToOneField('account.User', on_delete=models.CASCADE,null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    photo = models.CharField(max_length=255,null=True, blank=True)
    location = models.CharField(max_length=255)
    





class Booked(models.Model):
    STATE_CHOICES = [
        ('REQUESTED', 'Requested'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
        ('COMPLETED', 'Completed'),
        ('NO_SHOW', 'No Show'),
        ('IN_PROGRESS', 'In Progress'),
    ]

    lawyer = models.ForeignKey('Lawyer', on_delete=models.CASCADE)
    customer = models.ForeignKey('account.User', on_delete=models.CASCADE)
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    state = models.CharField(max_length=12, choices=STATE_CHOICES, default='REQUESTED')