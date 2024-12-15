from django.urls import include, path
from rest_framework import routers

from order import views


router = routers.DefaultRouter()
router.register(r'orders', views.OrderViewSet)
urlpatterns = [
    path('', include(router.urls)),
    
]