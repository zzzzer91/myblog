from django.contrib import admin

from .models import Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'name', 'created_time']
    list_filter = ['post']


admin.site.register(Comment, CommentAdmin)