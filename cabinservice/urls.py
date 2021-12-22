from django.urls import path, include
from django.conf.urls import url
from . import views
from rest_framework import routers
from .views import OrderViewSet, ServicesViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'services', ServicesViewSet)

urlpatterns = [
    url('loggedin/orderreceived/', views.new_order, name='new_order'),
    url('loggedin/orderdeleted/', views.delete_order, name='delete_order'),
    url('loggedin/orderupdated/', views.update_order, name='update_order'),
    url('loggedin/', views.login, name='login'),
    path('cabinservice/api/', include(router.urls)),
    path('', views.index, name='index')
]
