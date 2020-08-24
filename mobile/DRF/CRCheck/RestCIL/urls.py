from django.urls import path
from RestCIL import views as RestCILAPIViews
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('RestCIL/', RestCILAPIViews.index),
    path('RestCILData/', RestCILAPIViews.getData),
    path('RestCILAPI_POSTCILA030M/', RestCILAPIViews.post_CILA030M),
    path('RestCILAPI_GETCILA020M/', RestCILAPIViews.get_CILA020M)
]