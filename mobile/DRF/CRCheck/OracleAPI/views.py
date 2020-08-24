# -*- coding: utf-8 -*- 

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from OracleAPI.models import OracleAPIDB
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from YUSCO.Util.crcheck_sendmail import CRcheck_Auth_MAIL

import json

@csrf_exempt
def get_MECH003M(request):
    location_code = request.GET.get('location_code')
    ck_date = request.GET.get('ck_date')
    emplno = request.GET.get('emplno')
    deptno = request.GET.get('deptno')
    print('GET Param location_code=',location_code)
    print('GET Param ck_date=',ck_date)
    print('GET Param emplno=',emplno)
    print('GET Param deptno=',deptno)
    if request.method == 'GET':
        loc_code_t = location_code.replace("|", "','")
        print('GET Param loc_code_t=',loc_code_t)

#        ck_status = OracleAPIDB.ck_getMECH003M(location_code=location_code,ck_date=ck_date)
#        print(ck_status[0][0])
#        if ck_status[0][0] > 0 :
#            oralceapi = OracleAPIDB.getMECH003M_detail(location_code=location_code,ck_date=ck_date)
#            print(oralceapi)
#        else:
#            oralceapi = OracleAPIDB.getMECH002M_detail(location_code=location_code, emplno=emplno)
#            print(oralceapi)
        oralceapi = OracleAPIDB.getMECH002M_detail(location_code=loc_code_t, emplno=emplno, deptno=deptno)
        print(oralceapi)

        return JsonResponse( oralceapi, safe=False)
    else:
        return HttpResponse('hi')


@csrf_exempt
def post_MECH003M(request):
    print(request.method)
    CKData = json.dumps(request.POST) 
#    print(CKData)

    if request.method == 'POST':
        status = OracleAPIDB.insMECH003M(CKData)
        #點檢設備異常時寄信至主管信箱
        if status == True:
            smail_status = CRcheck_Auth_MAIL(CKData)
        return JsonResponse( request.POST, safe=False )
    else:
        return JsonResponse( 'hi', safe=False )


@csrf_exempt
def post_IMAGES(request):
    print(request.method)
    CKData = json.dumps(request.POST) 
#    CKData = request.POST.get("IMAGE01")
#    print(CKData)
#    text_file = open("sample.txt", "w")
#    n = text_file.write(CKData)
#    text_file.close()

    if request.method == 'POST':
        status = OracleAPIDB.saveIMAGES(CKData)
        return JsonResponse( 'success', safe=False )
    else:
        return JsonResponse( 'hi', safe=False )


@csrf_exempt
@api_view(('POST','GET'))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_IMAGES(request):
    print(request.method)

    if request.method == 'POST':
        CKData = json.dumps(request.POST) 
        print(CKData)
        result = OracleAPIDB.getIMAGES(CKData)
        return HttpResponse(result)
    elif request.method == 'GET':
        CKData = json.dumps(request.GET) 
        print(CKData)
        result = OracleAPIDB.getIMAGES(CKData)
        return HttpResponse(result)
    else:
        return JsonResponse( 'hi', safe=False )
