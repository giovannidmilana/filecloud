from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .forms import ImageForm, DocumentForm, MultiFileForm, DirForm, TitleForm
from .models import *
###
from django.template import RequestContext
import os
from wsgiref.util import FileWrapper
import mimetypes
import urllib 
from django.http import HttpResponse
from django.utils.encoding import smart_str
from PIL import Image
import shutil

# Create your views here.

def photo_save(request):
    if request.method != 'POST':
        # No data submitted create a blank form.
        form  = ImageForm()
    else:
        #POST data submitted; process data.
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            #m = Image.objects.get(pk=course_id)
            #m.model_pic = form.cleaned_data['image']
            #m.save()
            new_image = form.save(commit=False)
            #new_image.id = 1
            new_image.save()
            context = {'form': form}
            return render(request, 'g_cloud/new_photo.html', context)
    
    context = {'form': form}
    return render(request, 'g_cloud/new_photo.html', context)
    
    
    
     
def file_upload(request):
    if request.method != 'POST':
        form = DocumentForm()
    else:
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = form.save(commit=False)
            new_file.save()
            context = {'form': form}
            return render(request, 'g_cloud/new_file.html', context)
    
    context = {'form': form}
    return render(request, 'g_cloud/new_file.html', context)
    
    
    
###
def multi_file(request):
    if request.method != 'POST':
        form = MultiFileForm()
    else:
        form = MultiFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('uploads')
        #print(files)
        if form.is_valid():
             for f in files:
                  file_instance = MultiFile(uploads=f)
                  print(f)
                  file_instance.save()
                                
    context = {'form': form}
    return render(request, 'g_cloud/multi_file.html', context)
    
    
def files_list(request):
    folders = []
    files = []
    context = {'total_files':os.listdir(settings.MEDIA_ROOT),'path':settings.MEDIA_ROOT}
    print(os.listdir(settings.MEDIA_ROOT))
    print(settings.MEDIA_ROOT)
    for i in os.listdir(settings.MEDIA_ROOT):
        path=settings.MEDIA_ROOT +'/'+ i
        if os.path.isdir(path):  
            c = {str(i): os.listdir(path)}
            folders.append(c)
        else:
            files.append(i)
            #print(c)
    context = {'folders' : folders, 'files' : files}
    return render(request, 'g_cloud/files_list.html', context)
    
    
    
def download(request, file_name, folder='0'):
    if folder != '0':
        file_path = settings.MEDIA_ROOT + folder + '/' + file_name
    else:
        file_path = settings.MEDIA_ROOT + file_name
    filename, file_extension = os.path.splitext(file_path)
    print(type(file_extension))
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        print(1)
        fl = Image.open(file_path)
        
    else:
        print(2) 
        fl = open(file_path, "r")
    file_wrapper = FileWrapper(file_path, 'rb')
    file_mimetype, _ = mimetypes.guess_type(file_path)
    #print(file_mimetype)
    response = HttpResponse(fl, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s/' % smart_str(file_name) 
    return response
    
    
def folder_list(request, folder, path=settings.MEDIA_ROOT):
    path=settings.MEDIA_ROOT +''+ folder  
    context = {'folder':os.listdir(path), 'path' : path, 'dir' : folder}
    print(os.listdir(path))
    print(folder)
    return render(request, 'g_cloud/folder_list.html', context)
    
    
def dir_upload(request):
    if request.method != 'POST':
         fl = DirForm()
         ttl = TitleForm()
    else:
        fl = DirForm(request.POST, request.FILES)
        ttl = TitleForm(data=request.POST)
        if fl.is_valid():
            for afile in request.FILES.getlist('directory'):          
                title = ttl.save(commit=False)
                new_file = DirUpload(directory = afile)
                new_file.save()
                title.doc = new_file                          
                title.save()
                #rename(title.title)
            rename(title.title)
            print(title.title)
    #rename(title.title)
    context = {'fl' : fl, 'ttl' : ttl}
    return render(request, 'g_cloud/dir_upload.html', context)
    
    

def rename(title):
    src = settings.MEDIA_ROOT + 'temp/'
    dst = settings.MEDIA_ROOT + title + '/'
    #print(scr)
    print(dst)
    os.rename(src, dst)    
    #shutil.rmtree(src)

def del_():
     images = Image.objects.all()
     for image in images:
         image.delete()
         print('...')
         
def del_dir():
    dirs = DirUpload.objects.all()
    for dir_ in dirs:
        #dir_.delete()
        print('dir')
        print(dir_.id)     

def test():
    titles = Title.objects.all()
    for title in titles:
        print('title')
        print(title.doc.id)



#del_()
#del_dir()
#test()
