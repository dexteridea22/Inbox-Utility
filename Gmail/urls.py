"""Gmail URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,re_path
from django.conf.urls import url,include
from django.conf import settings
from .views import home_page
from gmailapi.views import gmail_authenticate,AutoReply

urlpatterns = [
    url(r'^$',home_page,name='home'),
    # path('Emails/', ListTableEmailsView,name='list'),
    url(r'^autoReply/$', AutoReply, name='auto_reply'),
    re_path('api/(?P<version>(v1|v2))/',include('gmailapi.urls')),
    url(r'^gmailAuthenticate/$', gmail_authenticate, name='gmail_authenticate'),
    path('admin/', admin.site.urls),
    
   

]
