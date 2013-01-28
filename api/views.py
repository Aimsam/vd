#-*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q
from admin.models import *
from django.core.cache import cache
import json
import service

PAGE_COUNT = 20
CACHE_KEY_VIDEO_LIST = "cache_key_video_list"
CACHE_KEY_VIDEO_KEYS = "cache_key_video_keys"
CACHE_KEY_VIDEO = "cache_key_video"


#id=2
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
        #@todo    
    if 'author' not in request.GET:
        author = 'all'  
        authorName = 'all'
    else:
        author = request.GET['author']
        try:
            authorObject = Author.objects.get(id=author)  
            authorName = authorObject.name
        except Author.DoesNotExist:
            return HttpResponse(json.dumps({'code':201, 'message':'error author id', 'author':author}, indent = 1))
    ##param check
    cacheKey = "%s_author_%s_page_%s_node_%s" % (CACHE_KEY_VIDEO_LIST, author, page, node)
    list = cache.get(cacheKey)
    if list is None:
        list = Video.objects.order_by("-published")
        if author != 'all':
            list = list.filter(author=author)
        list = list.all()
        paginator = Paginator(list, PAGE_COUNT)
        try:
            list = paginator.page(page)
        except :
            return HttpResponse(json.dumps({'code':202, 'message':'error page number', 'max_num':paginator.num_pages}, indent = 1))
        cache.set(cacheKey, list, 24*3600)
    videoList = []
    for video in list:
        increment = getIncrementById(video.id)
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
                     'love' : video.love + increment['love'],
                     'click' : video.click + increment['click']
                     }
        videoList.append(video_tmp)
    data = {'code':200, 'message':'success', 'author':authorName, 'node':'dota', 'list':videoList}   
    return HttpResponse(json.dumps(data, indent = 1, sort_keys=False))

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
       response.set_cookie("jz", "1", max_age=1)
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
            response.write(json.dumps(result, indent = 1))
            return response
    else:
        data['love']  += 1 
        cache.set(cacheKey, data)
    result = {"code":100, "message":"success", "id":id, "love":data['love']}
    response.write(json.dumps(result, indent = 1))
    return response

def getIncrementById(id):
    #return 1
    cacheKey = "%s_loveclick_id_%s" % (CACHE_KEY_VIDEO, id)
    data = cache.get(cacheKey)
    if data is None:
        data = {'love' : 0, 'click' : 0}
        cache.set(cacheKey, data)
        keys = cache.get(CACHE_KEY_VIDEO_KEYS)
        if keys is None:
            keys = [id]
        else:
            keys.append(id) 
        cache.set(CACHE_KEY_VIDEO_KEYS, keys)    
    return data

def hello(request):
    #cache.set("test", 10, timeout=3)
    cache.incr("test")
    #time.sleep(10)
    return HttpResponse(cache.get("test"))

def forceRefresh(request):
    
    cache.clear()
    
    return HttpResponse("success")


