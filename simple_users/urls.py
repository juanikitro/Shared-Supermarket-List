from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.SimpleUserCreateAPIView.as_view()),
    path("login/", views.login_simulation),
]
