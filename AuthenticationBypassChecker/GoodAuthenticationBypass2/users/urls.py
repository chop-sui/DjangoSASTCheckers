from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.CreateUser.as_view(), name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('findpassword/', views.FindPassword.as_view(), name='findpassword')
]