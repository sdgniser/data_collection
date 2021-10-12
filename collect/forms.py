from django import forms

from .models import Applicant

class UploadForm(forms.Form):
    BLOOD_GROUPS = (
        ('Opos', 'O +ve'),
        ('Oneg', 'O -ve'),
        ('Apos', 'A +ve'),
        ('Aneg', 'A -ve'),
        ('Bpos', 'B +ve'),
        ('Bneg', 'B -ve'),
        ('ABpos', 'AB +ve'),
        ('ABneg', 'AB -ve'),
    )

    app_no = forms.CharField(max_length=10, label='Application Number:', required=True)
    name = forms.CharField(max_length=100, required=True)
    photo = forms.ImageField(label='Upload your picture from Camera:', required=True)
    blood_group = forms.CharField(max_length=6, label='Blood Group:', required=True, widget=forms.Select(choices=BLOOD_GROUPS))
    raw_sign = forms.CharField(widget=forms.HiddenInput(), required=True)
