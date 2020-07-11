from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CreateUserView, ActivateUserView


router = DefaultRouter()
router.register('activate', ActivateUserView, basename="ActivateUserView")

urlpatterns = [
    path('create/', CreateUserView.as_view()),
]

urlpatterns += router.urls