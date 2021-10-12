from django.conf import settings
from django.core.files import File
from django.shortcuts import render


from .models import Applicant
from .forms import UploadForm

# Resource: https://stackoverflow.com/questions/34447308/how-to-save-jpeg-binary-data-to-django-imagefield
import re
from io import BytesIO
from base64 import decodestring

# Crop around signature: https://stackoverflow.com/questions/33998364/crop-image-from-all-sides-after-edge-detection
# Modified to fit usecase
import cv2
import numpy as np

def _crop(img):
    """
    Utility function to remove extra whitespace from signatures

    """
    canny = cv2.Canny(img, 400, 500) # Tweak minVal, maxVal to tune thresholds for edge detection

    # Find the non-zero min-max coords of canny
    pts = np.argwhere(canny > 0)
    y1, x1 = pts.min(axis=0)
    y2, x2 = pts.max(axis=0)

    # Crop the region & add a 15px border
    cropped = img[y1:y2, x1:x2]
    cropped = cv2.copyMakeBorder(
        cropped, 15, 15, 15, 15, cv2.BORDER_CONSTANT, value=[255,255,255]
    )

    is_success, buffer = cv2.imencode(".png", cropped)
    return BytesIO(buffer)


def Upload(request):
    """
    File Upload View

    """
    if request.method == 'POST': # POST
        form = UploadForm(request.POST, request.FILES)

        if form.is_valid():
            raw_sign_data = form.cleaned_data['raw_sign']
            data_url_pattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
            raw_sign = data_url_pattern.match(raw_sign_data).group(2)
            raw_sign = bytes(raw_sign, 'UTF-8')
            raw_sign = decodestring(raw_sign)

            sign_img_io = BytesIO(raw_sign)
            # Cropping in memory
            sign_img_io = _crop(cv2.imdecode(np.frombuffer(sign_img_io.read(), np.uint8), 1))
            sign_img_file = File(sign_img_io)
            sign_img_file.name = "sign.png"

            appl_obj = Applicant.objects.filter(app_no__exact=form.cleaned_data['app_no'])

            if appl_obj:  # Application Number exists
                appl_obj[0].name = form.cleaned_data['name'].upper()
                appl_obj[0].photo = form.cleaned_data['photo']
                appl_obj[0].blood_group = form.cleaned_data['blood_group']

                appl_obj[0].sign = sign_img_file

                appl_obj[0].save()

                message = "Old data has been overwritten!"
                message_color = "#dbd137"

                return render(request, 'base.html', context = {'form': UploadForm(), 'message': message, 'message_color': message_color})

            # Application Number does not exist
            appl_obj = Applicant()

            appl_obj.app_no = form.cleaned_data['app_no'].upper()
            appl_obj.name = form.cleaned_data['name'].upper()
            appl_obj.blood_group = form.cleaned_data['blood_group']
            appl_obj.photo = form.cleaned_data['photo']

            appl_obj.sign = sign_img_file

            appl_obj.save()

            message = "Data successfully uploaded."
            message_color = "#18b518"

            return render(request, 'base.html', context = {'form': form, 'message': message, 'message_color': message_color})

        else:
            message = ("Form invalid!" + str(form.errors)) if settings.DEBUG else "Form invalid!"
            return render(request, 'base.html', context = {'form': UploadForm(), 'message': message,})

    else: # GET & others
        return render(request, 'base.html', context = {'form':  UploadForm(),})
