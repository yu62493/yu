from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from CRLogin.models import CRUser
from CRLogin.serializers import CRLoginSerializer


@csrf_exempt
def crlogin_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        crlogin = CRUser.objects.all()
        serializer = CRLoginSerializer(crlogin, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CRLoginSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def crlogin_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        crlogin = CRUser.objects.get(pk=pk)
    except crlogin.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = CRLoginSerializer(crlogin)
        print(crlogin.emplno)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = CRLoginSerializer(crlogin, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        CRUser.delete()
        return HttpResponse(status=204)


@csrf_exempt
def crlogin_emplno(request):
    """
    List all code snippets, or create a new snippet.
    """
    emplno = request.GET.get('emplno')
    print(emplno)
    crlogin = CRUser.objects.all()
    serializer = CRLoginSerializer(crlogin, many=True)
    return JsonResponse(serializer.data, safe=False)

