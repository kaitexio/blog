"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from accounts import views as accounts_views
from rest_framework import routers
from blogs.urls import views
from blogs.urls import router as blog_router

router = routers.DefaultRouter()
router.register('users', views.PostViewSet)
router.register('comment', views.CommentViewSet)

urlpatterns = [
    path('signup/', accounts_views.signup, name='signup'),
    path('blogs/', include('blogs.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(blog_router.urls)),
    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
