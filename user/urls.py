from django.urls import path
from . import views
#url configuration , this file we map url
urlpatterns=[
    path('users/', views.user_list_create, name='user-list-create'),
    path('users/<int:user_id>/', views.user_detail_update_delete, name='user-detail-update-delete'),
] 