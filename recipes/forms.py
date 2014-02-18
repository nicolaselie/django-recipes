from django.contrib.comments.forms import CommentForm
from django.forms import CharField, Textarea

from .models import MarkdownComment

class MarkdownCommentForm(CommentForm):
    def __init__(self, *args, **kwargs):
        super(MarkdownCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = Textarea(attrs={'data-provide': 'markdown'})
        
    def get_comment_model(self):
        return MarkdownComment