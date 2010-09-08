from django.forms import ModelForm
from comment.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'url', 'comment', 'content_type', 'object_id')
