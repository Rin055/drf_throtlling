from django.urls import path
from .views import PostListView, PostCreateView

urlpatterns = [
    path('posts/', PostListView.as_view()),
    path('posts/create/', PostCreateView.as_view()),
]