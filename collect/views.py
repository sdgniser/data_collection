from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse

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
                old_name = appl_obj[0].name # will be used for checking if data is being over-written
                appl_obj[0].name = form.cleaned_data['name'].upper()
                appl_obj[0].photo = form.cleaned_data['photo']

                raw_sign_data = form.cleaned_data['raw_sign']
                data_url_pattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
                raw_sign = data_url_pattern.match(raw_sign_data).group(2)
                raw_sign = bytes(raw_sign, 'UTF-8')
                raw_sign = decodestring(raw_sign)
                img_io = BytesIO(raw_sign)
                appl_obj[0].sign.save("sign.png", File(img_io))

                if old_name == 'default-name':
                    message = "Data successfully uploaded."
                    message_color = "#18b518"
                else:
                    message = "The old data has been over-written"
                    message_color = "#dbd137"

                return render(request, 'base.html', context = {'form': form, 'message': message, 'message_color': message_color})

            else: # Application Number does not exist
                message = "Application Number not found !!!"
                message_color = "#f03030"
                return render(request, 'base.html', context = {'form': form, 'message': message, 'message_color': message_color})

        else:
            message = "Form invalid!" + str(form.errors) if settings.DEBUG else "Form invalid!"
            return render(request, 'base.html', context = {'form': UploadForm(), 'message': message,})

    else: # GET & others
        return render(request, 'base.html', context = {'form':  UploadForm(),})

def ValidateAppNo(request):
    """For the ajax thing of the name of application being filled"""
    appl_obj = Applicant.objects.filter(app_no__exact=request.GET.get("app_no", None))
    data = {
        'is_filled' : appl_obj[0].name != 'default-name'
        }
    return JsonResponse(data)
