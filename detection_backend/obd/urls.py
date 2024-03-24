from django.urls import path
from . import views

urlpatterns = [
    path('detectobjects/', views.detect_objects, name='detectobjects'),

]