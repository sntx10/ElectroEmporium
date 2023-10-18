from django.urls import path
from rest_framework.routers import DefaultRouter

from applications.orders import views

router = DefaultRouter()
router.register('', views.OrderViewSet)

urlpatterns = [
    path('confirm/<uuid:confirm_code>/', views.OrderConfirm.as_view()),
]
urlpatterns += router.urls
