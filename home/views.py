from django.shortcuts import render

# Create your views here.

def index (request):
    """returns index page"""
    
    return render(request, 'home/index.html')

def contact (request):
    """returns contact page"""
    
    return render(request, 'home/contact.html')

def about (request):
    """returns about page"""
    
    return render(request, 'home/about.html')
