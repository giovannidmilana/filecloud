from django import forms
from django.forms import ClearableFileInput
from .models import ImagePhoto, Document, MultiFile, DirUpload, Folder
from django.contrib.auth.models import User


'''
class ImageForm(forms.ModelForm):
    folder = forms.ModelChoiceField(queryset=Folder.objects.filter(owner=18),
                                    to_field_name = 'folder',
                                    empty_label="Select Folder")
    class Meta:
        model = ImagePhoto
        fields = ['photo', 'folder',]
        photo = forms.ImageField()
    
    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('request',None)
         super(ImageForm, self).__init__(*args, **kwargs)
'''
class ImageForm(forms.ModelForm):
    class Meta:
        model = ImagePhoto
        fields = ('photo', 'folder',)

    def __init__(self, user, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=user.id)

         
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload', 'folder',)
    
    def __init__(self, user, *args, **kwargs):
        super(DocumentForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(owner=user.id)

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
     


