from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from TinyTest.models import CRlogin
from TinyTest.serializers import TinyTestSerializer, LoginSerializer
from rest_framework import viewsets

from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer

from django.template.loader import get_template

# Create your views here.
class TinyTestViewSet(viewsets.ModelViewSet):
    queryset = CRlogin.objects.all()
    serializer_class = TinyTestSerializer

@csrf_exempt
def raw_sql_query(request):
    emplno = request.GET.get('emplno')
    password = request.GET.get('password')
    print('GET Param emplno=',emplno)
    print('GET Param password=',password)
    if request.method == 'GET':
        crlogin = CRlogin.fun_raw_sql_query(emplno=emplno)
        login_status = CRlogin.login_check(emplno=emplno)
        for p in crlogin:
            print(p.emplno)
        serializer = TinyTestSerializer(crlogin, many=True)
        test = LoginSerializer(crlogin, many=True)
        return JsonResponse( {'user': serializer.data}, safe=False)
#        return HttpResponse(login_status)
    elif request.method == 'POST':
        crlogin = CRlogin.login_check(emplno=emplno, password=password)
        serializer = TinyTestSerializer(crlogin, many=True)
        return JsonResponse( {'user': serializer.data}, safe=False)
#        return JsonResponse(serializer.data, safe=False)
#        return HttpResponse(login_status)
    else:
        return HttpResponse('hi')

@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def test001(request):
    emplno = request.GET.get('emplno')
    crlogin = CRlogin.fun_raw_sql_query(emplno=emplno)
    serializer = TinyTestSerializer(crlogin, many=True)
    print(serializer.data)
#    response = Response(serializer.data, template_name='test.html')
#    response['Access-Control-Allow-Origin'] = '*'
#    return response

    t = get_template("test.html") ##get_template() 方法可以直接得到人Template 实例,但是这个不是django.template.Template实例
    html = t.render({'now':serializer.data})
    return HttpResponse(html)
    

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")



