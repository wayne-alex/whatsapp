from django.urls import path

from . import views

urlpatterns = [

    path('', views.landing, name='landing'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('verify/', views.verify, name='verify'),
    path('forgot-password/', views.forgotpassword, name='forgot-password'),
    path('change-email/', views.changeEmail, name='change-email'),
    path('chats/', views.chats, name='chats'),
    path('profile/', views.profile, name='profile'),
    path('chat/<int:conversation_id>/', views.chat, name='chat'),

]
