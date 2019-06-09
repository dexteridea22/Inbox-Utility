from rest_framework import serializers
from .models import Emails
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class EmailsSerializer(serializers.ModelSerializer):
	# is_devoteful	=	serializers.BooleanField(read_only=True)
	# description		=	serializers.CharField(min_length=2,max_length=200)
	class Meta:
		model = Emails
		fields = ('Msg_id','Date','From','Subject','Message')
       