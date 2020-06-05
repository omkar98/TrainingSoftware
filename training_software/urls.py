from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_portal.urls')),
    path('register/', user_views.register, name='user-register'),
    path('dashboard/', user_views.user_dashboard, name='user-dashboard'),
    path('login/', user_views.user_login, name='user-login'),
    path('logout/', user_views.logout_view, name='user-logout'),
    path('addUpdate/', user_views.add_update, name='add-update'),
]
