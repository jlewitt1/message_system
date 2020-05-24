from django.urls import path
from message_api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('message/', views.handle_given_message),
    path('message/<str:get_all_messages>/', views.query_messages),
    path('api-token-auth/', obtain_auth_token),
]
