from django.urls import path
from .views import CreateUserView, ActivateUserView


urlpatterns = [
    path('create/', CreateUserView.as_view()),
    path('activate/', ActivateUserView.as_view({'post': 'create'}))
]
