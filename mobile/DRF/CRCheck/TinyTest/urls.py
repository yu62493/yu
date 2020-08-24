from django.urls import path, include
from TinyTest import views as TinyTestViews
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'TinyTest', TinyTestViews.TinyTestViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
#    path('tinytest/', views.TinyTestViewSet),
    path('tinytest_index/', TinyTestViews.index),
    path('tinytest_emplno/', TinyTestViews.raw_sql_query),
    path('tinytest_emplno2/', TinyTestViews.test001),
]