from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.users.api.v1.viewsets import SignupViewSet, LoginViewSet, ChangePasswordView

router = DefaultRouter()
router.register("signup", SignupViewSet, basename="signup")
router.register("login", LoginViewSet, basename="login")

urlpatterns = [
    path("", include(router.urls)),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
