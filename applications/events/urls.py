from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import EventCreateView, EventRetrieveDestroyUpdateView, EventListView


router = DefaultRouter()
router.register(r'', EventListView, basename="EventListView")

urlpatterns = [
    path('create/', EventCreateView.as_view()),
    path('<int:pk>/', EventRetrieveDestroyUpdateView.as_view()),
]

urlpatterns += router.urls
