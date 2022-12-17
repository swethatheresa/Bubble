from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in, name="signin"),
    path('logout/', views.logoutUser, name="logout"),
    path('signup/', views.sign_up, name="signup"),
    path('join/<str:pk>/', views.join, name="join"),
    path('room/<str:pk>/', views.room_details, name="room_details"),
    path('home/',views.home, name="home"),
    path('room/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('create-post/', views.createPost, name="create-post"),
    # path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    # path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    # path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    # path('update-user/', views.updateUser, name="update-user"),

    # path('topics/', views.topicsPage, name="topics"),
    # path('activity/', views.activityPage, name="activity"),
]