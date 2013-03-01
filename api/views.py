#-*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse
import service


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
    if '_force_refresh_' in request.GET:
        return HttpResponse(service.get_list_update(page, node, author))
    return HttpResponse(service.get_list(page, node, author))

#id = 1
def love(request, id):
    if '_update_' in request.GET:
        return HttpResponse(service.love_update())

    return service.love(request, id)

def love_update():

    return None



#id = 2
def get_author_list(request):
    return None


