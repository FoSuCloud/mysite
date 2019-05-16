from django.contrib import admin
from  .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id','content_type', 'object_id','comment_time','user')


