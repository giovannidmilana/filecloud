from django.contrib.auth.models import User
from django.db import models
#from django.conf import settings
#from django.core.files.storage import FileSystemStorage
from django import forms
###
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.

class Folder(models.Model):
     folder = models.CharField(max_length=30)
     owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
     def __str__(self):
         return self.folder

class ImagePhoto(models.Model):
    photo = models.ImageField(upload_to = 'files/', default = 'media/images/users.jpg')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    def get_photo_url(self):
        if self.photo and hasattr(self.photo, 'url'):
            return self.photo.url
        else:
            return "images/users.png"
    def filename(self):
        print(self.photo.name)
        return os.path.basename(self.photo.name)

class Document(models.Model):
    upload = models.FileField(upload_to='files/', default = 'media/images/users.jpg')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    def filename(self):
        print(self.upload.name)
        return os.path.basename(self.upload.name)

class MultiFile(models.Model):
    uploads = models.FileField(upload_to='files/', default = 'media/images/users.jpg')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    def filename(self):
        print(self.uploads.name)
        return os.path.basename(self.uploads.name)

class DirUpload(models.Model):
    directory = models.FileField(upload_to='files/', default = 'media/images/users.jpg')
    title =  models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    def filename(self):
        print(self.directory.name)
        return os.path.basename(self.directory.name)


     
     

     
