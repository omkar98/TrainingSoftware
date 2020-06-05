from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='portal-home'),
    path('participants/', views.participants, name='portal-participants'),
    path('announcements/', views.announcements, name='portal-announcements'),
    path('schedule/', views.schedule, name='portal-schedule'),
    path('downloads/', views.downloads, name='portal-downloads'),
    path('gallery/', views.gallery, name='portal-gallery'),
    path('contacts/', views.contacts, name='portal-contacts'),
]
