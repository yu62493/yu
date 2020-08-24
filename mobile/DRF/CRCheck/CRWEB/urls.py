from django.urls import path, include
from CRWEB import views as CRWEBViews


urlpatterns = [
    path('CRWEB_showPhotos/', CRWEBViews.show_PHOTOS),
]