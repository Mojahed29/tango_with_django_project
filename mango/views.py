from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("mango says hey there partner!")
