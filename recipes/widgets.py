from django.contrib.admin.widgets import AdminFileWidget, AdminTextInputWidget
from django.utils.safestring import mark_safe
from django.conf import settings

STATIC_URL = settings.STATIC_URL.rstrip('/')

class PreviewAdminImageWidget(AdminFileWidget):
    """Custom Image widget based on easy-thumbnails image widget which add image preview.
    http://www.psychicorigami.com/2009/06/20/django-simple-admin-imagefield-thumbnail/"""
    def render(self, name, value, attrs=None):
        if value and getattr(value, "url", None):
            output= u"<a href='%s'><img src='%s' /></a>" % \
                (value.url, value['thumbnail'].url)
        output += super(AdminFileWidget, self).render(name, value, attrs)
        return mark_safe(output)
        
class AdminDurationWidget(AdminTextInputWidget):
    class Media:
        js = ('%s/js/jquery-ui-django.js' % STATIC_URL,
              '%s/js/spinner.js' % STATIC_URL)
        css = {
            'all': ('%s/js/jquery-ui.css' % STATIC_URL,)
        }
        
    def __init__(self, attrs=None):
        final_attrs = {'class': 'vTextField spinner'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(AdminDurationWidget, self).__init__(attrs=final_attrs)