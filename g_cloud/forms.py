from django import forms
from django.forms import ClearableFileInput
from .models import Image, Document, MultiFile, DirUpload, Title

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['photo']
        #photo = forms.ImageField(label = 'Choose your image',  help_text = 'The image should be cool.')
        photo = forms.ImageField()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload',)


class MultiFileForm(forms.ModelForm):
    class Meta:
        model = MultiFile
        fields = ['uploads',]
        widgets = {
            'uploads': ClearableFileInput(attrs={'multiple': True}),
        }
        
        
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs=
        {'multiple': True, 'webkitdirectory': True, 'directory': True}))
        
        
class DirForm(forms.ModelForm):
    class Meta:
        model = DirUpload
        fields = ('directory',)
        
        
class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = ('title',)
        


