from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def privacy(request):
    return render(request, 'main/privacy.html')
