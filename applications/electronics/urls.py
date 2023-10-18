from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('', views.ElectronicViewSet, basename='electronic')

urlpatterns = [
    path('recommend/', views.ElectronicRecommendApiView.as_view()),
]

urlpatterns += router.urls
