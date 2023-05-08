from django import forms
from .models import *

class VaccineCentreForm(forms.ModelForm):
    class Meta:
        model = VaccineCentre
        fields = '__all__'
       
class DosageForm(forms.ModelForm):
    class Meta:
        model = Dosage
        fields = ['name','dose_amount', 'date']

class VaccineCentreForm(forms.ModelForm):
    class Meta:
        model = VaccineCentre
        fields = ('name', 'address', 'district', 'phone_number', 'email')


        
class BookingForm(forms.Form):
    aadhar_card_number = forms.CharField(max_length=12, label='Aadhar Card Number')
    is_vaccinated = forms.BooleanField(label='Are you already vaccinated?', required=False)

class SlotForm(forms.ModelForm):
    class Meta:
        model = Slot
        fields = ('vaccine_centre', 'date', 'available_slots')