from django.urls import path
from users.views import UserRegisterView, UserAuthView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from users.views import SimpleJWTView
from users.oauth_login import GoogleLoginOauth
from users.redis_code import GenerateCode, ConfirmCode

urlpatterns = [
    path("register/", UserRegisterView.as_view()),
    path("authenticate/", UserAuthView.as_view()),
    path('api/token/', SimpleJWTView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('google_login/', GoogleLoginOauth.as_view()),
    path('generate_code/', GenerateCode.as_view()),
    path('confirm_code/', ConfirmCode.as_view())
]