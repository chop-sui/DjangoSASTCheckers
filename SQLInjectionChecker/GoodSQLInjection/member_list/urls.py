from django.urls import path
from . import views

urlpatterns = [
    path('safe1/<str:user_name>', views.safe_get_users1, name='safe_get_users1'),
    path('safe2/<str:user_name>', views.safe_get_users2, name='safe_get_users2'),
    path('safe3/<str:user_name>', views.safe_get_users3, name='safe_get_users3'),
]