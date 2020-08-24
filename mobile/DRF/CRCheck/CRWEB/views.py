from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests

from django.template.loader import get_template


@csrf_exempt
def show_PHOTOS(request):
    LOCATION_CODE = request.GET.get('LOCATION_CODE')
    CK_DATE = request.GET.get('CK_DATE')
    CK_TIME = request.GET.get('CK_TIME')
    print('GET Param location_code=',LOCATION_CODE)
    print('GET Param ck_date=',CK_DATE)
    print('GET Param ck_time=',CK_TIME)

    if request.method == 'POST':
        r = requests.post('http://172.16.5.20:3000/OracleAPI_GETIMAGES', params=request.POST)
    else:
        r = requests.get('http://172.16.5.20:3000/OracleAPI_GETIMAGES', params=request.GET)
    if r.status_code == 200:
        print(r.content.decode("utf-8"))
        t = get_template("CRWEB_PHOTOS.html") ##get_template() 方法可以直接得到人Template 实例,但是这个不是django.template.Template实例
        html = t.render({'img':r.content.decode("utf-8") })
        return HttpResponse(html)
#        return HttpResponse(r)
    return HttpResponse('Could not save data')
