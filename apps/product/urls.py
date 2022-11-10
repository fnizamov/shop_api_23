from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, 'product')
router.register('categories', CategoryViewSet, 'category')

urlpatterns = [
    
]
urlpatterns += router.urls