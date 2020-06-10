from django.contrib import admin
from .models import Update, UserDetail, Issue, Solution

class UpdateView(admin.ModelAdmin):
    list_display = [
        'title',
        'student',
        'date_posted'
    ]
class IssueView(admin.ModelAdmin):
    list_display = [
        'title',
        'student',
        'date_posted'
    ]
class SolutionView(admin.ModelAdmin):
    list_display = [
        'issue',
        'date_posted',
        'mentor',
    ]
class UserDetailView(admin.ModelAdmin):
    list_display = [
        'student',
        'student_class',
        'status'
    ]

admin.site.register(Update, UpdateView)
admin.site.register(Issue, IssueView)
admin.site.register(Solution, SolutionView)
admin.site.register(UserDetail, UserDetailView)
