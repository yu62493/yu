# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from RestCIL.models import RestCILDB

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

import json

# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def getData(requet):
    RestCILDB.getData()
    print('aaa')
    return HttpResponse('hi')

@csrf_exempt
def post_CILA030M(request):
    print(request.method)
#    ckremark = request.POST.get("CK_REMARK")
#    print(ckremark)
    CKData = json.dumps(request.POST) 
    print(CKData)
    if request.method == 'POST':
        status = RestCILDB.insCILA030M(CKData)
        return JsonResponse( request.POST, safe=False )
    else:
        return JsonResponse( 'hi', safe=False )

@csrf_exempt
def get_CILA020M(request):
    if request.method == 'GET':
        RestCILapi =  RestCILDB.getCILA020M()
        return JsonResponse(RestCILapi, safe=False)
    else:
        return HttpResponse('hi')