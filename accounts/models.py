from django.db import models

# Create your models here.


class EmailVerification(models.Model):
    email = models.CharField(max_length=500, null=True, blank=True)
    otp = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f'{self.email}'
    
