from django import forms
from .models import EventBooking, BookingAddon, Addon

# Event Booking Form
class EventBookingForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label="Event Date"
    )
    timing = forms.ChoiceField(
        choices=[
            ('11:30 AM - 01:30 PM', '11:30 AM - 01:30 PM'),
            ('02:00 PM - 04:00 PM', '02:00 PM - 04:00 PM'),
            ('05:00 PM - 07:00 PM', '05:00 PM - 07:00 PM'),
            # Add more timings as needed
        ],
        widget=forms.RadioSelect,
        label="Select Timing"
    )

    class Meta:
        model = EventBooking
        fields = ['fname', 'event_date', 'timing', 'email', 'phone', 'no_of_people', 'decoration']
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
            'no_of_people': forms.Select(attrs={'class': 'form-control'}),
            'decoration': forms.Select(attrs={'class': 'form-control'}),
        }


# Booking Addon Form (optional if you want to select addons)
class BookingAddonForm(forms.ModelForm):
    addon = forms.ModelChoiceField(
        queryset=Addon.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Select Addons"
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width:80px; display:inline-block; margin-left:10px;'})
    )

    class Meta:
        model = BookingAddon
        fields = ['addon', 'quantity']
