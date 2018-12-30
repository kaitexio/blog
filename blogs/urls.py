from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from .views import PostViewSet, CommentViewSet


app_name = 'blog'

router = routers.DefaultRouter()
router.register('posts', PostViewSet)
router.register('comment', CommentViewSet)

urlpatterns = [
    path('', views.HomeView.as_view(), name='Home'),
    path('user/<int:user_id>/', views.AccountArticleView.as_view(), name='account_article'),
    path('user/post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path ('post/new',views.NewPostView.as_view(), name='post_new'),
    path('post/<int:pk>/edit', views.post_edit, name='post_edit'),
    path('post/<pk>/remove/', views.post_remove, name='post_remove'),
    path('comment/<int:pk>/', views.CommentView.as_view(), name='comment'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('top/', views.top_page, name="top"),
    path('tweet/', views.AccountView.as_view(), name='accounts'),
 ]
