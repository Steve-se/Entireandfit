from django.urls import path
from .views import user_login, register, logout_user

app_name = 'account'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', register, name='register' )
   
]
