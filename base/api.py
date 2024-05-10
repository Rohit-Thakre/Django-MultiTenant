from django.shortcuts import HttpResponse

def Home(request):
    return HttpResponse("Hello World")