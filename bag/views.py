from django.shortcuts import render

def bag (request):
    """returns bag page"""
    
    return render(request, 'bag/bag.html')