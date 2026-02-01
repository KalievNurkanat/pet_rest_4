from django.urls import path
from users_part.views import UserRegisterView, UserAuthView

urlpatterns = [
    path("register/", UserRegisterView.as_view()),
    path("authenticate/", UserAuthView.as_view())
]