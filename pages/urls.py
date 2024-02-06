from django.urls import path
from .views import *


urlpatterns = [
    path('', home_page, name='home'),
    path('register/', register_page, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', user_logout, name='logout'),
    path('create/', create_page, name='create'),
    path('all_pages/', all_pages, name='all_pages'),
    path('detail_page/<int:page_id>/', detail_page, name='detail_page'),
    path('delete_page/<int:page_id>/', delete_page, name='delete_page'),
    path('edit_page/<int:page_id>/', edit_page, name='edit_page'),
    path('random_page/  ', random_page, name='random_page'),
]