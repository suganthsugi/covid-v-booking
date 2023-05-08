from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class VaccineCentre(models.Model):
    name = models.CharField(max_length=100)
    address= models.TextField()
    district=models.CharField(max_length=25)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    

    def __str__(self):
        return self.name

    


class Dosage(models.Model):
    centre = models.ForeignKey(VaccineCentre, on_delete=models.CASCADE)
    COVISHIELD = 'Covishield'
    COVAXINE = 'Covaxine'
    SPUTNIK_V = 'Sputnik-V'

    NAME_CHOICES = (
        (COVISHIELD, 'Covishield'),
        (COVAXINE, 'Covaxine'),
        (SPUTNIK_V, 'Sputnik-V'),
    )
    name = models.CharField(max_length=100, choices=NAME_CHOICES)
    dose_amount = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return self.name


class Slot(models.Model):
    vaccine_centre = models.ForeignKey(VaccineCentre, on_delete=models.CASCADE)
    date = models.DateField()
    available_slots = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return f"{self.vaccine_centre.name} - {self.date}"

class UserData(models.Model):
    aadhar_number = models.CharField(max_length=12)
    is_booked = models.BooleanField(default=False)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    center = models.ForeignKey(VaccineCentre, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Reduce the available slot count for the booked center by 1
        VaccineCenter.objects.filter(id=self.center.id).update(slots_available=F('slots_available') - 1)
        super().save(*args, **kwargs)
