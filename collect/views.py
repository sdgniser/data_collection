from django.shortcuts import render, redirect
from django.conf import settings

from .models import Applicant
from .forms import UploadForm

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
                appl_obj[0].sign = form.cleaned_data['sign']
                appl_obj[0].save()
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
