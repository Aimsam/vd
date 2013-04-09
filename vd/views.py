from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.cache import cache
import os
from django.core.context_processors import csrf


def index(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('index.html', c)