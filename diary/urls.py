from django.urls import path
from . import views

urlpatterns = [
    path('', views.trip_list, name='trip_list'),
    path('my/', views.my_trips, name='my_trips'),
    path('trip/<int:pk>/', views.trip_detail, name='trip_detail'),
    path('trip/create/', views.trip_create, name='trip_create'),
    path('trip/<int:pk>/edit/', views.trip_edit, name='trip_edit'),
    path('trip/<int:pk>/delete/', views.trip_delete, name='trip_delete'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]