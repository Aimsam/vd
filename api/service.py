__author__ = 'aimsam'
from django.core.paginator import Paginator
from admin.models import *
from django.core.cache import cache
from django.http import HttpResponse
import urllib
import json

PAGE_COUNT = 20
CACHE_KEY_VIDEO_LIST = "cache_key_video_list"
CACHE_KEY_VIDEO_KEYS = "cache_key_video_keys"
CACHE_KEY_VIDEO = "cache_key_video"
CACHE_KEY_VIDEO_LIST_KEYS = "cache_key_video_list_keys"
CACHE_KEY_AUTHOR_LIST = "cache_key_author_list"
CACHE_KEY_AUTHOR_KEYS = "cache_key_author_keys"

def fresh_list(node, author):
    list = Video.objects.filter(node = node).all()
    paginator = Paginator(list, PAGE_COUNT)
    page_num = paginator.num_pages
    for i in range(1, page_num):
        cacheKey = "%s_author_%s_page_%s_node_%s" % (CACHE_KEY_VIDEO_LIST, author, i, node)
        cache.delete(cacheKey)
    #@todo
    return True

def get_list(page, node, author):
    authorName = author
    cacheKey = "%s_author_%s_page_%s_node_%s" % (CACHE_KEY_VIDEO_LIST, author, page, node)
    list = cache.get(cacheKey)
    if list is None:
        print "from database" #@todo debug message
        if authorName != 'all':
            try:
                authorObject = Author.objects.get(id=author)
                authorName = authorObject.name
            except Author.DoesNotExist:
                return json.dumps({'code':201, 'message':'error author id', 'author':authorName}, indent = 1)

        list = Video.objects.order_by("-published")
        if author != 'all':
            list = list.filter(author=author)
        list = list.all()
        paginator = Paginator(list, PAGE_COUNT)
        try:
            list = paginator.page(page)
        except :
            return json.dumps({'code':202, 'message':'error page number', 'max_num':paginator.num_pages}, indent = 1)
        cache.set(cacheKey, list, 24*3600)
    else:
        print "from cache" #@todo debug message
    videoList = []
    for video in list:
        increment = get_increment_byid(video.id)
        print increment
        video_tmp = {'id' : video.id,
                     'author':video.author.id,
                     'user' : video.user.name,
                     #'tag':video.tags,
                     'title' : video.title,
                     'thumbnail' : video.thumbnail,
                     'quality' : video.quality,
                     'duration' : video.duration,
                     'published' : video.published.strftime("%Y-%m-%d"),
                     'description' : video.description,
                     'remarks' : video.remarks,
                     'love' : video.love + increment['love'],
                     'click' : video.click + increment['click']
        }

        videoList.append(video_tmp)
    data = {'code':200, 'message':'success', 'author':authorName, 'node':'dota', 'list':videoList}
    return json.dumps(data, indent = 1, sort_keys=False)

def get_increment_byid(id):
    cacheKey = "%s_love_click_id_%s" % (CACHE_KEY_VIDEO, id)
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

#click love
def love(request, id):
    response =  HttpResponse("")
    if id is None or id == "":
        result = {"code":101, "message":"id is empty", "id":id}
        response.write(json.dumps(result, indent = 1))
        return response
    if "aaa" in request.COOKIES:
        result = {"code":103, "message":"too fast", "id":id}
        response.write(json.dumps(result, indent = 1))
        return response
    else:
        response.set_cookie("aaa", "2", max_age = 60)
    cacheKey = "%s_love_click_id_%s" % (CACHE_KEY_VIDEO, id)
    data = cache.get(cacheKey)
    if data is None:
        try:
            data = Video.objects.get(id=id)
            data.love += 1
            data = {"love":data.love, "click":data.click}
            cache.set(cacheKey, data)
            keys = cache.get(CACHE_KEY_VIDEO_KEYS)
            if keys is None:
                keys = [id]
            else:
                keys.append(id)
            cache.set(CACHE_KEY_VIDEO_KEYS, keys)
        except Video.DoesNotExist:
            result = {"code":102, "message":"error id", "id":id}
            response.write(json.dumps(result, indent = 1))
            return response
    else:
        data['love']  += 1
        print data
        cache.set(cacheKey, data)
    result = {"code":100, "message":"success", "id":id, "love":data['love']}
    response.write(json.dumps(result, indent = 1))
    return response

#save love increment into database
def love_update():
    keys = cache.get(CACHE_KEY_VIDEO_KEYS)
    if keys is None:
        return False
    for row in keys:
        video = Video.objects.get(id=row)
        cacheKey = "%s_love_click_id_%s" % (CACHE_KEY_VIDEO, row)
        data = cache.get(cacheKey)
        if data['love'] >= 1:
            video.love += data['love']
            video.love
            video.save()
        cache.delete(cacheKey)
    cache.delete(CACHE_KEY_VIDEO_KEYS)
    cache.delete_pattern(CACHE_KEY_VIDEO_LIST + "*")#clear list cache

    return True

def get_author_list():
    cacheKey = CACHE_KEY_AUTHOR_LIST
    list = cache.get(cacheKey)
    if list is None:
        print "from database"#@todo debug message
        list = Author.objects.filter(node=1).all()
        cache.set(cacheKey, list)
    else:
        print "from cache"
    authorList = []
    for author in list:
        tmp = {
            'id' : author.id,
            'name' : author.name,
            'description' : author.description,
            'avatar' : author.avatar,
            'love' : author.love,
        }
        authorList.append(tmp)
    return json.dumps({"code" : 300, "message" : "success", "list" : authorList}, indent = 1)

#follow the authors id = 4
def follow(request, author_id, author_name):
    response =  HttpResponse("")
    if "follow_dict" in request.COOKIES:
        try:
            follow_str = request.COOKIES["follow_dict"]
            follow_str = urllib.unquote(follow_str)
            follow_dict = eval(follow_str)
            print follow_dict
        except:
            response.set_cookie("follow_dict", None, path="/")
            response.write(json.dumps({"code" : 401, "message" : "cookies error"}))

    else:
        follow_dict = {}
    if follow_dict.has_key(author_id) is False:
        follow_dict[author_id] = {"last_view" : 9999999999, 'author_name' : author_name}
        response.set_cookie("follow_dict", follow_dict)
        response.write(json.dumps({"code" : 4001, "cookies" : str(follow_dict), "message" : "success follow", "author_id": author_id, "author_name" : author_name}, indent = 1))
    else:
        del follow_dict[author_id]
        response.set_cookie("follow_dict", follow_dict)
        response.write(json.dumps({"code" : 4002, "cookies" : str(follow_dict), "message" : "success unfollow", "author_id": author_id, "author_name" : author_name}, indent = 1))
    return response





