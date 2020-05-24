from django.urls import path
from message_api import views

urlpatterns = [
    path('', views.sanity_check),
    path('message/', views.write_new_message),
    # path('documents_web/<int:company_id>/', views.check_document_status),
    # path('documents_web/document/<str:document_id>/<str:document_status>/<str:model_type>/',
    #      views.retrieve_document_data),
    # path('documents_web/document/user/', views.update_user_feedback),
    # path('documents_web/document/user/approve_all/', views.update_all),
    # path('documents_web-delete/<str:document_id>/', views.documents_web_delete),
]
