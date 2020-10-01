from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static 

app_name = 'cloud'

urlpatterns = [
    path('g_cloud/', views.index, name='index'),
    #path('files_list/<str:path>/', views.download, name='download'),
    #path('files_list/<str:file_name>/', views.download, name='download'),
    #path('folder_list/<str:file_name>/<str:path>/', views.download, name='download'),
    #path('files_list/<str:file_name>/', views.download, name='download'),
    #path('', views.folder_list, name='folder_list'),
    
    path('folder_list1/<str:file_name>/<str:folder>/', views.download),
    
    path('files_list2/<str:file_name>/<str:folder>/', views.download),
    
    path('files_list/<str:folder>/', views.folder_list, name='folder_list'),

    path('files_list/', views.files_list, name='files_list'),
    path('files_list4/', views.files_list, name='files_list'),
    #path('', views.files_list, name='files_list'),
    
    
    path('files_list5/<str:file_name>/', views.download),
    path('<str:file_name>/str:path>/', views.download, name='download'),
    path('files_list6/<str:file_name>/<str:folder>/', views.download, name='download'),
    #path('download/', views.download, name='download'),
    #path('', views.download, name='download'),
    
    #path('', views.index, name='index'),
    path('photo_save/', views.photo_save, name='save'),
    path('', views.photo_save, name='save'),
    path('file_upload/', views.file_upload, name='file_upload'),
    path('', views.file_upload, name='file_upload'),
    path('multi_file/', views.multi_file, name='multi_file'),
    path('', views.multi_file, name='multi_file'),
    
    path('dir_upload/', views.dir_upload, name='dir_upload'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static('/templates/', document_root=settings.PROJECT_DIR + '/templates/')
