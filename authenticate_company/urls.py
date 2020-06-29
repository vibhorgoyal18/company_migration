from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from authenticate_company import views

# API endpoints
urlpatterns = format_suffix_patterns([
    path('auth-server', views.Login.as_view()),
    path('server-info', views.GetServerInfo.as_view()),
    path('re-auth-server', views.ReAuthServer.as_view()),
])
