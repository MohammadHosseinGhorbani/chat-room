from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.sign_up, name='sign_up'),
    path('signup/code/<str:email>$<str:username>/', views.code, name='code'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.HomePage.as_view(), name='home_page'),
    path('create/', views.create, name='create'),
    path('home/room<str:invite_link>/', views.room(False), name='room'),
    path('home/room<str:invite_link>/ajax', views.room(True), name='room_ajax'),
    path('home/send/', views.send, name='send'),
    path('home/leave/', views.leave, name='leave'),
    path('home/delete-room/', views.delete_room, name='delete_room'),
    path('home/kick/', views.kick_user, name='kick_user'),
    path('home/setadmin/<str:status>/', views.set_room_administration, name='set_admin')
]
