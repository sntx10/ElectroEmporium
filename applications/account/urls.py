from django.urls import path
from django.views.decorators.cache import cache_page
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.account import views

urlpatterns = [
    path('login/', cache_page(60*5)(TokenObtainPairView.as_view()), name='token_obtain'),
    path('refresh/', cache_page(60*5)(TokenRefreshView.as_view()), name='token_refresh'),
    path('register/', cache_page(60*5)(views.RegisterApiView.as_view())),
    path('activate/<uuid:activation_code>/', views.ActivationApiView.as_view()),
    path('change_password/', views.ChangePasswordApiView.as_view()),
    path('forgot_password/', views.ForgotPasswordApiView.as_view()),
    path('forgot_password_confirm/', views.ForgotPasswordConfirmApiView.as_view()),
    path('forgot_password_codeword/', views.ForgotPasswordCodewordApiView.as_view()),
    path('forgot_password_phone/', views.ForgotPasswordPhoneApiView.as_view())
]