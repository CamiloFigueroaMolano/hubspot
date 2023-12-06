from django.urls import path
from . import views
from .views import list_users, update_user, delete_user, add_user
urlpatterns = [
    path('add/', add_user, name='add_user'),
    path('list_users/', list_users, name='list_users'),
    path('update/<int:user_id>/', update_user, name='update_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),

]
