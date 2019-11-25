from django.shortcuts import render
from django.http import HttpResponse
from .crawl import crawl_url_list


# Create your views here.
def crawl(request):
    crawl_url_list()
    return HttpResponse("Hello, world. I am Festa Crawler")
