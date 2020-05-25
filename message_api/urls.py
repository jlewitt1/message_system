from django.urls import path
from message_api import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('message/', views.handle_given_message),
    path('message/<int:message_id>/', views.handle_given_message),
    path('message/query/', views.query_messages),
    path('message/query/<str:message_type>/', views.query_messages),
    path('message/delete/<str:user_type>/', views.remove_message),
    path('message/delete/id/<int:message_id>/', views.remove_message),
    path('api-token-auth/', obtain_auth_token),
]
