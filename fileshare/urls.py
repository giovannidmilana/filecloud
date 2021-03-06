"""fileshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from g_cloud import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    #path('', include('g_cloud.urls', namespace='g_cloud')),    
    path('g_cloud/', include('g_cloud.urls', namespace='g_cloud')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#urlpatterns += static('/templates/', document_root=settings.PROJECT_DIR + '/templates/')

#print(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
