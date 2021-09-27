from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(Task)

