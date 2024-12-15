from django.urls import include, path
from rest_framework import routers

from product import views

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewset)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    
]