from django.contrib import admin

# Register your models here.
from  gmailapi.models import Emails,AutoReplyIds

admin.site.register(Emails)
admin.site.register(AutoReplyIds)