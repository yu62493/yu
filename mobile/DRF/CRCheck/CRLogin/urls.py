from django.urls import path
from CRLogin import views

urlpatterns = [
    path('crlogin/', views.crlogin_list),
    path('crlogin/<int:pk>/', views.crlogin_detail),
    path('crlogin_test/', views.crlogin_emplno),
]