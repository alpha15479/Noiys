from django.urls import path
from django.contrib.auth.views import LogoutView
from django.utils.regex_helper import next_char
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='post_list'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    path('home', home,name='home'),
    path('post/', post,name='post'),
    path('task/<int:pk>/', TaskDetail.as_view() ,name='task'),
    path('task/', TaskList.as_view() ,name='tasks'),
    path('task-create/', TaskCreate.as_view() ,name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view() ,name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view() ,name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
    
    path('', post_list ,name='post_list'),
    path('about', about, name='about'),
    path('like/<int:id>', LikeView, name='like_post'),
    path('task/<int:id>',post_detail ,name='post-detail'),
    path('profile/', profile ,name='profile'),
] 
 