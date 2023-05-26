
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from .views import register, password_reset, add_user, list_all_items, add_item


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', password_reset, name='password_reset'),
    path('register/', register, name='register'),
    path('add_user/', add_user, name='add_user'),
    path('list_items/', list_all_items, name='list_all_items'),
    path('add_item/', add_item, name='add_item')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)