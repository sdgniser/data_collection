from django import forms

from .models import Applicant

class UploadForm(forms.Form):
    app_no = forms.CharField(max_length=10, label='Application Number:', required=True)
    name = forms.CharField(max_length=100, required=True)
    photo = forms.ImageField(label='Upload your picture from Camera:', required=True)
    sign = forms.ImageField(label='Upload your signature from Signature Pad:', required=True)
