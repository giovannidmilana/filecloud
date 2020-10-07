from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views

app_name = 'cloud'

urlpatterns = [
    path('folder_list/<int:file_name>/', views.download, name='download'),
    path('', views.photo_save, name='photo_save'),
    path('', views.new_folder, name='new_folder'),
    path('', views.file_upload, name='file_upload'),
    path('photo_save/', views.photo_save, name='photo_save'),
    path('new_folder/', views.new_folder, name='new_folder'),
    path('file_upload/', views.file_upload, name='file_upload'),
    path('test/', views.index, name='index'),
    path('', views.index, name='index'),
    path('g_cloud/', views.index, name='index'),
    
    path('files_list/<int:f>/', views.folder_list, name='folder_list'),
    path('files_list4/', views.files_list, name='files_list'),
    
    path('multi_file/', views.multi_file, name='multi_file'),
    path('', views.multi_file, name='multi_file'),
    path('dir_upload/', views.dir_upload, name='dir_upload'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='g_cloud/login.html'), name='login'),
    
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

