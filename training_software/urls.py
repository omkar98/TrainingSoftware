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
    path('addIssue/', user_views.add_issue, name='add-issue'),
    path('getUpdates/', user_views.get_updates, name='get-updates'),
    path('updateEmails/', user_views.updates_email, name='update-emails'),
    path('viewEmail/', user_views.viewemailtemplate, name='view-emails'),
    path('noUpdatedStudents/', user_views.no_updates_email, name='not-updated'),

]
