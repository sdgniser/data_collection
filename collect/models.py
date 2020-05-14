from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os

def set_photo(obj, filename):
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    filename = f'{obj.pk}-photo.{ext}'

    return os.path.join(upload_to, filename)

def set_sign(obj, filename):
    upload_to = 'sign'
    ext = filename.split('.')[-1]
    filename = f'{obj.pk}-sign.{ext}'

    return os.path.join(upload_to, filename)

class Applicant(models.Model):
    app_no = models.CharField(verbose_name='Application Number', max_length=10, blank=False, primary_key=True)
    name = models.CharField(max_length=100, blank=False, null=False, default='default-name')
    photo = models.ImageField(upload_to=set_photo, blank=False, null=False, default='default.png')
    sign = models.ImageField(upload_to=set_sign, blank=False, null=False, default='default.png')

    class Meta:
        ordering = ['app_no']

    def __str__(self):
        return f'{self.app_no} | {self.name}'


# Orphaned File Deletion
# https://stackoverflow.com/questions/16041232/django-delete-filefield?answertab=votes#tab-top
@receiver(pre_save, sender=Applicant)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_photo = Applicant.objects.get(pk=instance.pk).photo
        old_sign = Applicant.objects.get(pk=instance.pk).sign
    except Applicant.DoesNotExist:
        return False

    new_photo = instance.photo
    new_sign = instance.sign
    if not old_photo == new_photo:
        if os.path.isfile(old_photo.path):
            #  Don't delete default files
            if 'default' in old_photo.path:
                return False
            os.remove(old_photo.path)

    if not old_sign == new_sign:
        if os.path.isfile(old_sign.path):
            #  Don't delete default files
            if 'default' in old_sign.path:
                return False
            os.remove(old_sign.path)


@receiver(post_delete, sender=Applicant)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.photo:
        #  Don't delete default files
        if 'default' in instance.photo.path:
            return False
        
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)
    
    if instance.sign:
        #  Don't delete default files
        if 'default' in instance.sign.path:
            return False

        if os.path.isfile(instance.sign.path):
            os.remove(instance.sign.path)

