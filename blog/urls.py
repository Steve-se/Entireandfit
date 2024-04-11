from django.urls import path
from .views import index, PostDetailView, contact_us

app_name = 'blog'

urlpatterns = [
    path('', index, name='homepage'),
    path('<str:slug>/', PostDetailView.as_view(), name='detail-page'), 
    path('contact', contact_us, name='contact')
   
]
