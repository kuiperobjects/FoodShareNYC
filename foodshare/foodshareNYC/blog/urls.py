from django.urls import path
from . import views
from .views import (calculate_distance_view, PostListView, 
	PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView)
from users import views as user_views
from django.conf.urls import include

import star_ratings.urls

#app_name = 'measurements'


urlpatterns = [
   path('', PostListView.as_view(), name = "FSNYC-home"),  
   path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
   path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
   path('post/new/', PostCreateView.as_view(), name='post-create'),
   path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
   path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
   path('main/', calculate_distance_view, name = "calculate-view"),
   path('about/', views.about, name = "FSNYC-about"),
   path('register/', user_views.register, name = "register"),
   #path('ratings/', star_ratings.urls, name='ratings'),
   path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),


]

