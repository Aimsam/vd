from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core.cache import cache
import os

def index(request):
    #print os.path.dirname(__file__) + "/template"
    list = cache.get("cache_key_video_list_author_all_page_1_node_1")
    return render_to_response('index.html', {'list':list})