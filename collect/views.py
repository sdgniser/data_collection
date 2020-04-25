from django.shortcuts import render, redirect
from django.conf import settings

from .models import Applicant
from .forms import UploadForm

# Resource: https://stackoverflow.com/questions/34447308/how-to-save-jpeg-binary-data-to-django-imagefield
# import re, io
import re
from io import BytesIO
from base64 import decodestring
from django.core.files import File

# Create your views here.
def Upload(request):
    """
    File Upload View

    """
    if request.method == 'POST': # POST
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            appl_obj = Applicant.objects.filter(app_no__exact=form.cleaned_data['app_no'])

            if appl_obj: # Application Number exists    
                appl_obj[0].name = form.cleaned_data['name'].upper()
                appl_obj[0].photo = form.cleaned_data['photo']
                
                raw_sign_data = form.cleaned_data['raw_sign']
                data_url_pattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
                raw_sign = data_url_pattern.match(raw_sign_data).group(2)
                raw_sign = bytes(raw_sign, 'UTF-8')
                raw_sign = decodestring(raw_sign)
                img_io = BytesIO(raw_sign)
                appl_obj[0].sign.save("sign.png", File(img_io))

                message = "Data succesfully uploaded."

                return render(request, 'base.html', context = {'form': form, 'message': message,})
            
            else: # Application Number does not exist
                message = "Application Number not found!"
                return render(request, 'base.html', context = {'form': form, 'message': message,})
            
        else:
            message = "Form invalid!" + str(form.errors) if settings.DEBUG else "Form invalid!"
            return render(request, 'base.html', context = {'form': UploadForm(), 'message': message,})
    
    else: # GET & others
        return render(request, 'base.html', context = {'form':  UploadForm(),})
