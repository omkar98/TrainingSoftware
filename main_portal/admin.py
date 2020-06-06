from django.contrib import admin
from .models import Update, UserDetail

class UpdateView(admin.ModelAdmin):
    list_display = [
        'title',
        'student',
        'date_posted'
    ]

class UserDetailView(admin.ModelAdmin):
    list_display = [
        'student',
        'student_class',
        'status'
    ]

admin.site.register(Update, UpdateView)
admin.site.register(UserDetail, UserDetailView)
