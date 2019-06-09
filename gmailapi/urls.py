from django.conf.urls import url
from django.urls import path
from .views import ListPaginatedEmailsView,gmail_authenticate


urlpatterns = [
    url(r'^gmailAuthenticate', gmail_authenticate, name='gmail_authenticate'),
     path('Emails/', ListPaginatedEmailsView.as_view(), name="Emails")
     # url(r'Emails/', Email_list, name='email'),
    ]
   