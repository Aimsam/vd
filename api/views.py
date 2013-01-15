#-*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from admin.models import *
from django.core.cache import cache
import json
import time
import datetime

PAGE_COUNT = 20
CACHE_KEY_VIDEO_LIST = "cache_key_video_list"
CACHE_KEY_VIDEO = "cache_key_video"



def get_list(request):
    if 'page' not in request.GET:
        page = 1
    else:
        page = request.GET['page']
        if not(page.isdigit()):
            page = 1
    if 'node' not in request.GET:
        node = 1
    else:
        node = request.GET['node']
        if not(node.isdigit()):
            node = 1      
    if 'author' not in request.GET:
        author = 'all'  
    else:
        author = request.GET['author']          
    ##param check
    cacheKey = "%s_author_%s_page_%s_node_%s" % (CACHE_KEY_VIDEO_LIST, author, page, node)
    list = cache.get(cacheKey)
    if list is None:
        list = Video.objects
        if author != 'all':
            list = list.filter(author=author)
        list = list.all()
        paginator = Paginator(list, PAGE_COUNT)
        list = paginator.page(page)
        videoList = []
        for video in list:
            video_tmp = {'id' : video.id,
                         #'author':video.author.id,
                         'user' : video.user.name,
                         #'tag':video.tags,
                         'title' : video.title,
                         'thumbnail' : video.thumbnail,
                         'quality' : video.quality,
                         'duration' : video.duration,
                         'published' : video.published.strftime("%Y-%m-%d"),
                         'description' : video.description,
                         'love' : video.love,
                         'click' : video.click
                         }
            videoList.append(video_tmp)
            
        list = videoList   
        #cache.set(cacheKey, videoList, 10)   
    for video in list:
        increment = getIncrementById(video['id'])
        video['click'] += increment['click']
        video['love'] += increment['love']
    
    data = {'list':list}   
    #return HttpResponse(list)
    return HttpResponse(json.dumps(data, indent = 1))

#id = 1
def love(request, id):
    response =  HttpResponse("")
    if id is None or id == "":
        result = {"code":101, "message":"id is empty", "id":id}
        response.write(json.dumps(result, indent = 1))
        return response
    if "jz" in request.COOKIES:
        result = {"code":103, "message":"too fast", "id":id}
        response.write(json.dumps(result, indent = 1))
        return response
    else:
       response.set_cookie("jz", "1", expires=datetime.now())
       
       
    cacheKey = "%s_loveclick_id_%s" % (CACHE_KEY_VIDEO, id)
    data = cache.get(cacheKey)
    if data is None:
        try:
            data = Video.objects.get(id=id)
            data.love += 1
            data = {"love":data.love, "click":data.click}      
            cache.set(cacheKey, data)
        except Video.DoesNotExist:
            result = {"code":102, "message":"error id", "id":id}
    else:
        data['love']  += 1 
        cache.set(cacheKey, data)
        result = {"code":100, "message":"success", "id":id, "love":data['love']}
        
#        if data is None:
#            result = {"code":102, "message":"error id"}
#            return HttpResponse(json.dumps(result, indent = 1))
        
    response.write(json.dumps(result, indent = 1))
    return response







def getIncrementById(id):
    cacheKey = "%s_loveclick_id_%s" % (CACHE_KEY_VIDEO, id)
    data = cache.get(cacheKey)
    if data is None:
        data = {'love' : 2, 'click' : 2}
        cache.set(cacheKey, data)
    return data


def hello(request):
    #cache.set("test", 10, timeout=3)
    cache.incr("test")
    #time.sleep(10)
    return HttpResponse(cache.get("test"))



