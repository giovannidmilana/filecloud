from django.db import models
#from django.conf import settings
#from django.core.files.storage import FileSystemStorage
from django import forms
###
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.

class Image(models.Model):
    #photo = models.ImageField(upload_to='customer/logo', storage=fs, null=True, blank=True)
    #photo = models.ImageField(upload_to='images/') 
    photo = models.ImageField(upload_to = 'images/', default = 'media/images/users.jpg')
    
    
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "images/users.png"


class Document(models.Model):
    upload = models.FileField(upload_to='uploads/', default = 'media/images/users.jpg')
    
    def get_document_url(self):
        if self.upload and hasattr(self.upload, 'url'):
            return self.upload.url
        else:
            return "files/users.png"


class MultiFile(models.Model):
    uploads = models.FileField(upload_to='files/', default = 'media/images/users.jpg')
    
    

class DirUpload(models.Model):
    directory = models.FileField(upload_to='temp/', default = 'media/images/users.jpg')
    #title =  models.CharField(max_length=30)
    
    
class Title(models.Model):
    title =  models.CharField(max_length=30)
    doc = models.ForeignKey(DirUpload, on_delete=models.CASCADE, null=True, blank=True)



