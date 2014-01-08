with open('static/js/jquery-ui.js', 'r') as f:
    data = f.read()
    
data = data.replace('( jQuery )', '( django.jQuery )')
data = data.replace('(jQuery)', '(django.jQuery)')
        
with open('static/js/jquery-ui-django.js', 'w') as f:
    f.write(data)