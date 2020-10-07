from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import ImageForm, DocumentForm, MultiFileForm, DirForm, FolderForm
from .models import *
from django.template import RequestContext
import os
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from django.http import FileResponse
import mimetypes
import urllib 
from django.http import HttpResponse
from django.utils.encoding import smart_str
from PIL import Image
#import PIL.Image
import shutil
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ImagePhoto, Document, MultiFile, DirUpload, Folder
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import (
    LoginView,
)
# Create your views here.

def index(request):
    #print('...')
    if request.user.is_authenticated:
        files = Folder.objects.filter(owner=request.user)
        context = {'files': files}
        return render(request, 'g_cloud/index.html', context)
    else:
        return render(request, 'g_cloud/test.html')

@login_required
def photo_save(request):
    if request.method != 'POST':
        # No data submitted create a blank form.
        form  = ImageForm()
    else:
        #POST data submitted; process data.
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.owner = request.user
            new_image.save()
            context = {'form': form}
            return render(request, 'g_cloud/new_photo.html', context)
    print(form)
    context = {'form': form}
    return render(request, 'g_cloud/new_photo.html', context)
    
    
    
@login_required
def file_upload(request):
    if request.method != 'POST':
        form = DocumentForm()
    else:
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.owner = request.user
            new_file.save()
            print(new_file.folder)
            context = {'form': form}
            return render(request, 'g_cloud/new_file.html', context)
    
    context = {'form': form}
    return render(request, 'g_cloud/new_file.html', context)
    
    
    
###
@login_required
def multi_file(request):
    if request.method != 'POST':
        form = MultiFileForm()
    else:
        form = MultiFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('uploads')
        #files = request.FILES
        print(files)
        if form.is_valid():
             for f in files:
                  file_instance = MultiFile(uploads=f)
                  file_instance.owner = request.user
                  file_instance.save()
             file_instance.save()                   
    context = {'form': form}
    return render(request, 'g_cloud/multi_file.html', context)
    
@login_required
def files_list(request):
    files = Folder.objects.filter(owner=request.user)
    context = {'files': files}
    return render(request, 'g_cloud/files_list.html', context)
    #return render(request, 'g_cloud/index.html', context)

@login_required    
def download(request, file_name):
    print(file_name)
    #t = ImagePhoto.objects.get(id=file_name)
    t = DirUpload.objects.get(pk=file_name)
    #i = t.photo.url.split('/')
    i = t.directory.url.split('/')
    file_path = settings.MEDIA_ROOT + i[-2] + '/' + i[-1]
    filename, file_extension = os.path.splitext(file_path)
    chunk_size = 8192
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        response = StreamingHttpResponse(FileWrapper(open(file_path, 'rb'), chunk_size),
                           content_type=mimetypes.guess_type(file_path)[0])
        response['X-SendFile'] = smart_str(i[-1])
        response['Content-Length'] = os.path.getsize(file_path)    
        response['Content-Disposition'] = "attachment; filename=%s" % i[-1]
        return response
    else:
        fl = open(file_path, "r")
    file_wrapper = FileWrapper(file_path, 'rb')
    file_mimetype, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type=file_mimetype )
    response['X-SendFile'] = smart_str(i[-1])
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(i[-1]) 
    return response
    
@login_required    
def folder_list(request, f, path=settings.MEDIA_ROOT):
    fldr = Folder.objects.get(id=f)
    i = ImagePhoto.objects.filter(folder=f, owner=request.user)
    d = Document.objects.filter(folder=f, owner=request.user)
    du = DirUpload.objects.filter(title=fldr.folder, owner=request.user)
    files = []
    files.append(i)
    files.append(d)
    files.append(du)
    for f in files:
        print(f)
    
    
    context = { 'files' : files }
    return render(request, 'g_cloud/folder_list.html', context)
    
@login_required    
def dir_upload(request):
    if request.method != 'POST':
         fl = DirForm()
    else:
        fl = DirForm(request.POST, request.FILES)
        if fl.is_valid():
            tmp = fl.save(commit=False)
            for afile in request.FILES.getlist('directory'):          
                new_file = DirUpload(directory = afile)
                new_file.title = tmp.title 
                new_file.owner = request.user
                new_file.save()
            f = Folder(folder=new_file.title, owner=request.user)
            folder = f.save()
    context = {'fl' : fl}
    return render(request, 'g_cloud/dir_upload.html', context)

@login_required
def new_folder(request):
    if request.method != 'POST':
        form = FolderForm()
    else:
        form = FolderForm(request.POST)
        if form.is_valid():
             new_folder = form.save(commit=False)
             new_folder.owner = request.user
             new_folder.save()
    context = {'form' : form}
    return render(request, 'g_cloud/new_folder.html', context)


def rename(title):
    src = settings.MEDIA_ROOT + 'temp/'
    dst = settings.MEDIA_ROOT + title + '/'
    os.rename(src, dst)    

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            # Log the user in, and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
                password=request.POST['password1'])
            f = Folder(folder='images', owner=new_user)
            folder = f.save()
            j = Folder(folder='files', owner=new_user)
            folder2 = j.save()
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('g_cloud:index'))

    context = {'form': form}
    return render(request, 'g_cloud/register.html', context)


class login_view(LoginView):
    template_name = 'g_cloud/login.html'


def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('g_cloud:index'))



def del_():
     images = ImagePhoto.objects.all()
     for image in images:
         image.delete()
         print('...')
         
def del_dir():
    dirs = DirUpload.objects.all()
    for dir_ in dirs:
        dir_.delete()
        print('dir')
        print(dir_.id)     

def del5_():
    fs = Folder.objects.all()
    for f in fs:
        f.delete()

def del2_():
     docs = Document.objects.all()
     for doc in docs:
         doc.delete()
         print('...')

def del3_():
     mfs = MultiFile.objects.all()
     for mf in mfs:
         mf.delete()
         print('...')

def del4_():
     users = User.objects.all()
     for user in users:
         user.delete()


     

#del5_()
#del4_()
#del2_()
#del3_()
#del_()
#del_dir()
#test()
