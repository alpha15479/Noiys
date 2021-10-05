from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin

class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'description', 'created_at')
admin.site.register(Task, TaskAdmin)

class CommentAdmin(MPTTModelAdmin):
    list_display = ('task','name', 'content', 'publish')
admin.site.register(Comment, CommentAdmin)
