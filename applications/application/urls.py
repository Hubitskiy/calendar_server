from django.contrib import admin
from django.urls import path, include

from users import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/jwt/create/', views.JWTAuthenticationView.as_view()),
    path('v1/users/', include('users.urls')),
    path('v1/events/', include('events.urls'))
]
