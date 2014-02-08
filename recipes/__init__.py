from .forms import MarkdownCommentForm
from .models import MarkdownComment

def get_form():
    #return PagedownCommentForm
    return MarkdownCommentForm

def get_model():
    return MarkdownComment