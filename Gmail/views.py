from django.shortcuts import render

# Create your views here.

def home_page(request):
	status = True
	context = {'status': status}
	return render(request,"base.html",context)
