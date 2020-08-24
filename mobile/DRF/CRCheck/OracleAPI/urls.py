from django.urls import path, include
from OracleAPI import views as OracleAPIViews
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('OracleAPI_MECH003M/', OracleAPIViews.get_MECH003M),
    path('OracleAPI_POSTMECH003M/', OracleAPIViews.post_MECH003M),
    path('OracleAPI_POSTIMAGES/', OracleAPIViews.post_IMAGES),
    path('OracleAPI_GETIMAGES/', OracleAPIViews.get_IMAGES),
]