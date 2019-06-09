from django.db import models

# Create your models here.

class Emails(models.Model):

	Mail_id 		= models.AutoField(primary_key=True)
	Msg_id 			= models.CharField(max_length=100,null=False)
	Date 			= models.CharField(max_length=100)
	From 			= models.CharField(max_length=100)
	Subject 		= models.TextField()
	Message        	= models.TextField()
	def __str__(self):
		return str(self.From)
class AutoReplyIds(models.Model):
	Reply_id= models.AutoField(primary_key=True)
	Msg_id 	= models.CharField(max_length=100,null=False)
	Label 	= models.CharField(max_length=100,null=False)
	Date    = models.CharField(max_length=100,null=False)
	From	= models.CharField(max_length=100)
	To      = models.CharField(max_length=100)
	Subject = models.TextField()
	Message = models.TextField()
	
	def __str__(self):
		return str(self.Msg_id)

