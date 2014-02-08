from django.contrib.comments.forms import CommentForm
from django.forms import CharField, Textarea

from .widgets import CommentPageDownWidget
from .models import MarkdownComment

class PagedownCommentForm(CommentForm):
    comment = CharField(widget=CommentPageDownWidget())
    
    def get_comment_model(self):
        return MarkdownComment

class MarkdownCommentForm(CommentForm):
    def __init__(self, *args, **kwargs):
        super(MarkdownCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = Textarea(attrs={'data-provide': 'markdown'})
        
    def get_comment_model(self):
        return MarkdownComment