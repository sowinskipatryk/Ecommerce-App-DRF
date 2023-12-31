from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.OrderViewSet)

urlpatterns = [
    path('stats/', views.MostSoldProductsView.as_view(), name='stats'),
    path('', include(router.urls)),
]
