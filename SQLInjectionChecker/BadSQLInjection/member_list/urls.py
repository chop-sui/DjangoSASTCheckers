from django.urls import path
from . import views

urlpatterns = [
    path('unsafe1/<str:user_name>', views.unsafe_get_users1, name='unsafe_get_users1'),
    path('unsafe2/<str:user_name>', views.unsafe_get_users2, name='unsafe_get_users2'),
    path('unsafe3/<str:user_name>', views.unsafe_get_users3, name='unsafe_get_users3'),
    path('unsafe4/<str:user_name>', views.unsafe_get_users4, name='unsafe_get_users4'),
    path('search/', views.SearchMember.as_view(), name='search'),
    path('create/', views.CreateMember.as_view(), name='create'),
]