from django.shortcuts import render

def index(request):
    return render(request, 'isearch/index.html')

def search(request):
    return render(request, 'isearch/search.html')