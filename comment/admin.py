from comment.models import Comment
from django.contrib import admin

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status', 'comment', 'created')
    search_fields = ['name', 'email']
    ordering = ['-created']
    
admin.site.register(Comment, CommentAdmin)