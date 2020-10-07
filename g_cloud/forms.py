from django import forms
from django.forms import ClearableFileInput
from .models import ImagePhoto, Document, MultiFile, DirUpload, Folder

class ImageForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.all(),
                                    to_field_name = 'folder',
                                    empty_label="Select Folder")
    class Meta:
        model = ImagePhoto
        fields = ['photo', 'folder',]
        photo = forms.ImageField()
        

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload', 'folder',)


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
        fields = ('title',)
        
      
class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('folder',)
     


