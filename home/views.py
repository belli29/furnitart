from django.shortcuts import render

# Create your views here.

def index (request):
    """returns index page"""
    
    return render(request, 'home/index.html')
