#-*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse
import service
from sphinx import Sphinx
import json
from django.core.context_processors import csrf
from django.shortcuts import render_to_response


#id=2
def get_list(request):
    if 'page' not in request.GET:
        page = 1
    else:
        page = request.GET['page']
        if not(page.isdigit()):
            page = 1
    if 'node' not in request.GET:
        node = 'all'
    else :
        node = request.GET['node']
#    else:
#        node = request.GET['node']
#        if not(node.isdigit()):
#            node = 1
            #@todo
    if 'author' not in request.GET:
        author = 'all'
    else:
        author = request.GET['author']
    if '_force_refresh_' in request.GET:
        return HttpResponse(service.fresh_list(node, author))

    return HttpResponse(service.get_list(page, node, author))

#id = 1
def love(request, id):
    if '_update_' in request.GET:
        return HttpResponse(service.love_update())
    return service.love(request, id)

def love_update():
    return service.love_update()

#id = 3
def get_author_list(request):
    if 'node' not in request.GET:
        return HttpResponse('jsonp3({"code":301, "message":"empty node number"})');
    else:
        node = request.GET['node']
        if not(node.isdigit()):
            node = 1
    if '_force_refresh_' in request.GET:
        return HttpResponse(service.fresh_author_list())
    return HttpResponse(service.get_author_list(node))

#id = 4
def follow(request):
    if not (request.POST.has_key('author_id') | request.POST.has_key('author_name')):
        return HttpResponse(json.dumps({'code' : 401, 'message' : 'author_id or author_name is not given'}, indent = 1))
    else :
        author_id = request.POST['author_id']
        author_name = request.POST['author_name']
    return service.follow(request, author_id, author_name)

def test(request):
    s = Sphinx()
    return HttpResponse(s.get_author_update_number(["蓝"], 1284652800))
    #callback = request.GET['callback']
    return HttpResponse("j(" + str({"code" :400}) +")")

def get_update_number(request):
    if 'follow_dict' not in request.GET:
        return HttpResponse("json({'code' : 501, 'message' : 'follow_dict not given'})")
    follow_dict = request.GET['follow_dict']
    s = Sphinx()
    return HttpResponse("jsonp5(" + s.get_author_update_number(follow_dict) + ")")