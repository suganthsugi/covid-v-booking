from django.shortcuts import render, redirect,get_object_or_404,reverse
from .models import *
from .forms import *
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail



def addcentre(request):
    if request.method == 'POST':
        form = VaccineCentreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listcentre')
    else:
        form = VaccineCentreForm()
    return render(request, 'addcentre.html', {'form': form})




def listcentres(request):
    district = request.GET.get('district')
    selected_date = request.GET.get('date')
    selected_date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date() if selected_date else None
    print(selected_date)
    selected_date_str_standard = selected_date.strftime('%Y-%m-%d') if selected_date else None
    print(selected_date_str_standard)
    # print(date_selected)
    # Get all the VaccineCentres in the given district
    vaccine_centres = VaccineCentre.objects.filter(district=district)

    # Get the available slots for the selected date
    available_slots = {}
    if selected_date:
        slots = Slot.objects.filter(date=selected_date)
        available_vaccine_centre_pks = [slot.vaccine_centre.pk for slot in slots if slot.available_slots > 0]
        available_vaccine_centres = VaccineCentre.objects.filter(pk__in=available_vaccine_centre_pks)
        vaccine_centres = vaccine_centres.intersection(available_vaccine_centres)
        for slot in slots:
            if slot.vaccine_centre in vaccine_centres:
                available_slots[slot.vaccine_centre.pk] = slot.available_slots
    
    for x in vaccine_centres:
        x.slots = Slot.objects.filter(vaccine_centre=x, date=selected_date).first().available_slots
    
    
    context = {
        'vaccine_centres': vaccine_centres,
        'selected_date': selected_date_str_standard,
        'district': district,
        'available_slots': available_slots,
    }

    return render(request, 'listcentre.html', context)   

    
     
def adminlistcentres(request):
    if request.user.is_authenticated:
        vaccine_centres = VaccineCentre.objects.all()
        context = {
            'vaccine_centres': vaccine_centres,
        }
        return render(request, 'adminlistcentres.html', context)
    else:
        return redirect('login')

def create_slot(request,pk):
    centre = get_object_or_404(VaccineCentre, pk=pk)
    if request.method == 'POST':
        form = SlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.vaccine_centre = centre
            slot.save()
            return redirect('slotlist', pk=pk)

    else:
        form = SlotForm()

    return render(request, 'create_slot.html', {'form': form, 'centre': centre})


    return redirect('listcentre')


def slot_update(request, pk):
    slot = get_object_or_404(Slot, pk=pk)
    if request.method == 'POST':
        form = SlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            messages.success(request, f'Slot updated successfully.')
            return redirect('adminlistcentre')
    else:
        form = SlotForm(instance=slot)
    return render(request, 'slot_update.html', {'form': form})

def slot_delete(request, pk):
    slot = get_object_or_404(Slot, pk=pk)
    if request.method == 'POST':
        slot.delete()
        messages.success(request, f'Slot deleted successfully.')
        return redirect('adminlistcentre')
    return render(request, 'slotdelete.html', {'slot': slot})


def updatecentre(request, pk):
    centre = get_object_or_404(VaccineCentre, pk=pk)
    form = VaccineCentreForm(request.POST or None, instance=centre)
    if form.is_valid():
        form.save()
        return redirect('adminlistcentre')
    return render(request, 'update_vaccine_centre.html', {'form': form, 'centre': centre})





def removecentre(request, pk):
    centre = get_object_or_404(VaccineCentre, pk=pk)
    if request.method == 'POST':
        centre.delete()
        return redirect('adminlistcentre')
    return render(request, 'removecentre.html', {'centre': centre})



def adddosage(request, pk):
    centre = get_object_or_404(VaccineCentre, pk=pk)
    if request.method == 'POST':
        form = DosageForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            dose_amount = form.cleaned_data['dose_amount']
            date = form.cleaned_data['date']
            
            dosage, created = Dosage.objects.get_or_create(
                centre=centre,
                name=name,
                defaults={ 'dose_amount': dose_amount, 'date': date}
            )
            
            if not created:
                dosage.dose_amount = F('dose_amount') + dose_amount
                dosage.save()
                
            
            return redirect('adminlistcentre')
    else:
        form = DosageForm()
    return render(request, 'adddosage.html', {'centre': centre, 'form': form})



def dosagelist(request, pk):
    centre = get_object_or_404(VaccineCentre, pk=pk)
    dosage_id = request.GET.get('id')
    if dosage_id:
        dosages = Dosage.objects.filter(centre=centre, id=dosage_id)
    else:
        dosages = Dosage.objects.filter(centre=centre)
    return render(request, 'dosage.html', {'centre': centre, 'dosages': dosages})



def bookslot(request):
    if request.method == 'POST':
        center_id = request.POST.get('centre_id')
        date_str = request.POST.get('date')
        aadhaar = request.POST.get('aadhaar')
        email=request.user.email
        # print(email)
        # print(date_str)
        # print(aadhaar)
        passcode=aadhaar[len(aadhaar)-4:len(aadhaar)]
        # print(passcode)
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Please use the YYYY-MM-DD format.')
            return redirect('listcentre')
        center = VaccineCentre.objects.filter(id=center_id)[:1].get()
        print(center)

        slots = Slot.objects.filter(vaccine_centre=center, date=date)
        if slots.exists():
            slot = slots.first()
            if slot.available_slots > 0:
                slot.available_slots -= 1
                slot.save()
                send_mail(
                "Covidvaccine Booking Confirmation",
                f"Your booking is confirmed on {date_str}"+f" in {center}"+f" Passcode:{passcode}",
                'covidvaccinebooking1@gmail.com',
                [email],
                fail_silently=False
        )
                # messages.success(request, f"Slot booked at {center.name} on {date}")
                return redirect('success')
            else:
                messages.error(request, f"No available slots at {center.name} on {date}")
        else:
            messages.error(request, f"No slots found at {center.name} on {date}")
            return redirect('confirmation')
    else:
        return redirect('listcentre')

def success(request):
    return render(request,'success.html')



def slotlist(request, pk):
    centre = get_object_or_404(VaccineCentre, pk=pk)
    slots = Slot.objects.filter(vaccine_centre=centre)
    return render(request, 'slot_list.html', {'centre': centre, 'slots': slots})






