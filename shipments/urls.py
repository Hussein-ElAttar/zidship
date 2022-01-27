"""zidship URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from shipments import views

urlpatterns = [
    path('', views.ShipmentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:pk>/', views.ShipmentViewSet.as_view({'get': 'retrieve'})),
    path('<int:pk>/print/', views.ShipmentViewSet.as_view({'get': 'print'})),
    path('<int:pk>/track/', views.ShipmentViewSet.as_view({'get': 'track'})),
    path('<int:pk>/cancel/', views.ShipmentViewSet.as_view({'post': 'cancel'})),

    path('statuses/', views.ShipmentStatusViewSet.as_view({'get': 'list'})),
    path('statuses/<int:pk>/', views.ShipmentStatusViewSet.as_view({'get': 'retrieve'})),

    path('methods/', views.ShipmentMethodViewSet.as_view({'get': 'list'})),
    path('methods/<int:pk>/', views.ShipmentMethodViewSet.as_view({'get': 'retrieve'})),

    path('couriers/', views.CourierViewSet.as_view({'get': 'list'})),
    path('couriers/<int:pk>/', views.CourierViewSet.as_view({'get': 'retrieve'})),
]
