import re
import markdown
from markdown.postprocessors import Postprocessor
from markdown.treeprocessors import Treeprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.blockprocessors import UListProcessor, OListProcessor
from markdown.extensions import Extension
from markdown.serializers import ElementTree
from markdown import util

from mdx_latex import _write_latex, HTMLTAG_TO_LATEXENV, to_latex_string

ALLOWED_UNITS = ['°C', 'h', 'min', 's', 'g', 'mg', 'cg', 'L', 'mL', 'cL', 'dL', 'verre']

# blah + text + ': ' + text (used in ingredients section)
INGREDIENTS_RE = re.compile('(?P<name>[^\:]+)\:\s(?P<quantity>.+)\\\\\\\\$')
# <li> + text + ': ' + text + </li> (used in ingredients section)
INGREDIENTS_HTML_RE = re.compile('<li>(?P<name>[^\:]+)\:\s(?P<quantity>.+)<\/li>$')
# blah + number + 0 or 1 space + allowed unit + end of line or non alphanumeric character
UNITS_RE = re.compile('(?P<value>[0-9]+)\s{0,1}(?P<unit>%s)(?=$|[^a-zA-Z]+)' 
                        % '|'.join(ALLOWED_UNITS))
# blah + number + / + number
FRAC_RE = re.compile('(?P<numerator>[0-9]+)/(?P<denominator>[0-9]+)')

HTMLTAG_TO_XCOOKYBOOKY = HTMLTAG_TO_LATEXENV.copy()
HTMLTAG_TO_XCOOKYBOOKY['ul[@id="ingredients"]'] = {'start': r'\ingredients' + '\n' + r'{%',
                                     'end':   r'}' + '\n'}
HTMLTAG_TO_XCOOKYBOOKY['ul[@id="ingredients"]/li'] = {'start': r'',
                             'end':   r'\\'}
HTMLTAG_TO_XCOOKYBOOKY['ol[@id="recipe"]'] = {'start': r'\preparation' + '\n' + r'{%',
                             'end':   r'}' + '\n'}
HTMLTAG_TO_XCOOKYBOOKY['ol[@id="recipe"]/li'] = {'start': r'\step ',
                             'end':   r''}

COOKING_SYMBOLS = { 'bottomheat': 'B',
                    'fanoven': 'F',
                    'gasstove': 'G',
                    'topbottomheat': 'H',
                    'bakingtime': 'O',
                    'topheat': 'T',
                    'portion': 'd',
                    'fork': 'f',
                    'preparationtime': 'g',
                    'knife': 'k',
                    'spoon': 's',
                    'source': 'p',
                    'temperature': 't'}

def has_meta_key(md, key):
    if key in md.Meta and md.Meta[key][0] != '':
        return True
    else:
        return False

def to_xcookybooky_string(element):
    return to_latex_string(element, convtable=HTMLTAG_TO_XCOOKYBOOKY)

### XCookyBooky Extension

def makeExtension(configs=None):
    return XCookyBookyExtension(configs=configs)

class XCookyBookyExtension (Extension):
    ''' XCookyBooky output extension for Python-Markdown. '''

    def extendMarkdown(self, md, md_globals):
        ''' Add LaTeXPreprocessor to Markdown instance. '''

        md.output_formats['xcookybooky'] = to_xcookybooky_string
        md.parser.blockprocessors.add('xcookybooky_ingredients',
                                      IngredientsListProcessor(md.parser),
                                      '_begin')
        md.parser.blockprocessors.add('xcookybooky_recipe',
                                      RecipeListProcessor(md.parser),
                                      '_begin')
        md.treeprocessors.add('xcookybooky',
                                XCookyBookyTreeprocessor(md),
                                '_begin')
        md.postprocessors.add('xcookybooky',
                              XCookyBookyPostprocessor(md),
                              '_begin')

class XCookyBookyTreeprocessor(Treeprocessor):
    def run(self, doc):
        md = self.markdown
        if md.output_format == 'xcookybooky':
            for elem in doc.getiterator():
                if elem.tag == 'ingredients':
                    elem.tag = 'ul'
                    elem.set('id', 'ingredients')
                elif elem.tag == 'recipe':
                    elem.tag = 'ol'
                    elem.set('id', 'recipe')
        else:
            for elem in doc.getiterator():
                if elem.tag == 'ingredients':
                    elem.tag = 'div'
                    elem.set('id', 'ingredients')
                    
                    subp = util.etree.SubElement(elem, 'p')
                    subp.text = 'Ingrédients'
                    
                    subelem = util.etree.SubElement(elem, 'ul')
                    for e in elem.findall('li'):
                        sube = util.etree.SubElement(subelem, 'li')
                        sube.text = e.text
                        elem.remove(e)
                elif elem.tag == 'recipe':
                    elem.tag = 'div'
                    elem.set('id', 'recipe')
                    
                    subp = util.etree.SubElement(elem, 'p')
                    subp.text = 'Préparation'
                    
                    subelem = util.etree.SubElement(elem, 'ol')
                    for e in elem.findall('li'):
                        sube = util.etree.SubElement(subelem, 'li')
                        sube.text = e.text
                        elem.remove(e)
        
    
class IngredientsListProcessor(UListProcessor):
    TAG = 'ingredients'
    RE = re.compile(r'^[ ]{0,3}[~][ ]+(.*)')
    CHILD_RE = re.compile(r'^[ ]{0,3}(([~]))[ ]+(.*)')
    SIBLING_TAGS = [TAG]
    
class RecipeListProcessor(UListProcessor):
    TAG = 'recipe'
    RE = re.compile(r'^[ ]{0,3}\d+\)[ ]+(.*)')
    CHILD_RE = re.compile(r'^[ ]{0,3}((\d+\)))[ ]+(.*)')
    SIBLING_TAGS = [TAG]

class XCookyBookyPostprocessor(Postprocessor):   
    def sub_units(self, g):
        unit = r'\textcelcius' if g.group('unit') == '°C' else g.group('unit')
        return r'\unit[%s]{%s}' % (g.group('value'), unit)
    
    def sub_frac(self, g):
        return r'$\frac{%s}{%s}$' % (g.group('numerator'), g.group('denominator'))
    
    def sub_ingredients(self, g):
        return g.group('quantity') + ' & ' + g.group('name') + r'\\'

    def sub_frac_html(self, g):
        return r'<sup>%s</sup>&frasl;<sub>%s</sub>' % (g.group('numerator'), g.group('denominator'))
    
    def sub_ingredients_html(self, g):
        return '<li><span class="left">%s</span><span class="right">%s</span></li>' % (g.group('quantity'), g.group('name'))
    
    def run(self, text):
        lines = []
        write = lines.append
        md = self.markdown
        
        if md.output_format == 'xcookybooky':
            write(r'\begin{recipe}')
            write(r'[ % ')
            
            if has_meta_key(md, 'preparationtime'):
                write(r'preparationtime = {%s},' % md.Meta['preparationtime'][0])
            else:
                write(r'preparationtime,')
                
            if has_meta_key(md, 'bakingtime'):
                write(r'bakingtime = {%s},' % md.Meta['bakingtime'][0])
            else:
                write(r'bakingtime,')

            temperatures = ''
            for mode in ['fanoven', 'topbottomheat', 'topheat', 'gasstove']:
                key = 'bakingtemperature{0}'.format(mode)
                if has_meta_key(md, key):
                    temperatures += mode.lower() + '=' + md.Meta[key][0].strip() + ', '
                else:
                    temperatures += mode.lower() + ', '
            write(r'bakingtemperature = {\protect\bakingtemperature{%s}},' % temperatures.strip(', '))
                
            if has_meta_key(md, 'portion'):
                write(r'portion = {%s},' % md.Meta['portion'][0])
            else:
                write(r'portion,')
                
            if has_meta_key(md, 'calory'):
                write(r'calory = %s,' % md.Meta['calory'][0])
            else:
                write(r'calory,')
                
            if has_meta_key(md, 'source'):
                write(r'source = %s' % md.Meta['source'][0])
            else:
                write(r'source,')
                
            write(r']')
            
            if has_meta_key(md, 'title'):
                write(r'{%s}' % md.Meta['title'][0])
            else:
                write(r'{}')
            
            if has_meta_key(md, 'smallpicture') or has_meta_key(md, 'bigpicture'):
                write(r'')
                write(r'\graph')
                write(r'{% pictures')
                
                if has_meta_key(md, 'smallpicture'):
                    write(r'small=%s,' % md.Meta['smallpicture'][0])
                else:
                    write(r'small,')
                    
                if has_meta_key(md, 'bigpicture'):
                    write(r'big=%s,' % md.Meta['bigpicture'][0])
                else:
                    write(r'big,')
                    
                write(r'}')
            
            if has_meta_key(md, 'hint'):
                write(r'')
                write(r'\hint')
                write(r'{%')
                for i, hint in enumerate(md.Meta['hint']):
                    if hint != '':
                        if i < len(md.Meta['hint'])-1:
                            hint += r'\\'
                        write(r'%s' % hint)
                write(r'}')
                write(r'')
        else:
            write(r'<!DOCTYPE html>')
            write(r'<html>')
            write(r'<head>')
            write(r'<meta charset="utf-8" />')
            write(r'<link rel="stylesheet" href="/stylesheet.css" type="text/css" />')
            
            if has_meta_key(md, 'title'):
                write(r'<title>%s</title>' % md.Meta['title'][0])
            else:
                write(r'<title></title>')
                
            write(r'</head>')
            write(r'')
            write(r'<body>')
            
            if has_meta_key(md, 'smallpicture') or has_meta_key(md, 'bigpicture'):
                write(r'<div id="images">')
                    
                if has_meta_key(md, 'bigpicture'):
                    write(r'<img src="%s.jpg" />' % md.Meta['bigpicture'][0])
                    
                if has_meta_key(md, 'smallpicture'):
                    write(r'<img src="%s.jpg" />' % md.Meta['smallpicture'][0])
                    
                write(r'</div>')
             
            if has_meta_key(md, 'title'):
                write(r'')
                write(r'<h1>%s</h1>' % md.Meta['title'][0])
                
            if has_meta_key(md, 'preparationtime') \
              or has_meta_key(md, 'bakingtime') \
              or has_meta_key(md, 'portion') \
              or has_meta_key(md, 'calory') \
              or has_meta_key(md, 'source'):
                write(r'')
                write('<div id="meta">')
                if has_meta_key(md, 'preparationtime'):
                    write('<p><span class="cookingsymbol">{0}</span>{1}</p>'\
                        .format(COOKING_SYMBOLS['preparationtime'], md.Meta['preparationtime'][0]))
                
                baking = '<p>'
                if has_meta_key(md, 'bakingtime'):
                    baking += '<span class="cookingsymbol">{0}</span>{1}, '\
                        .format(COOKING_SYMBOLS['bakingtime'], md.Meta['bakingtime'][0])
                
                temperatures = ''
                for mode in ['fanoven', 'topbottomheat', 'topheat', 'gasstove']:
                    key = 'bakingtemperature{0}'.format(mode)
                    if has_meta_key(md, key):
                        temperatures += '{0}<span class="cookingsymbol">{1}</span>, ' \
                            .format(md.Meta[key][0], COOKING_SYMBOLS[mode])
                
                if temperatures != '':
                    baking += '<span class="cookingsymbol">{0}</span>'\
                        .format(COOKING_SYMBOLS['temperature']) + temperatures.strip(', ')
                    
                baking += '</p>'
                write(baking)
                
                if has_meta_key(md, 'portion'):
                    write(r'<p><span class="cookingsymbol">{0}</span>{1}</p>' \
                        .format(COOKING_SYMBOLS['portion'], md.Meta['portion'][0]))
                    
                if has_meta_key(md, 'calory'):
                    write(r'<p><span class="cookingsymbol">{0}</span>{1}</p>' \
                        .format('Calories', md.Meta['Calories'][0]))
                    
                if has_meta_key(md, 'source'):
                    write(r'<p><span class="cookingsymbol">{0}</span>{1}</p>' \
                        .format(COOKING_SYMBOLS['source'], md.Meta['source'][0]))
                
                write(r'</div>')
                write(r'')
        
        lines += text.split('\n')
        
        if md.output_format == 'xcookybooky':
            level = 0
            in_ingredients = False
            for i, line in enumerate(lines):
                #Apply some regex replace: \unit, tabular organization in ingredients and \frac
                line = UNITS_RE.sub(self.sub_units, line)
                if in_ingredients == False:
                    if line.startswith(r'\ingredients'):
                        in_ingredients = True
                elif in_ingredients == True:
                    if line.startswith('}'):
                        in_ingredients = False
                    else:
                        line = INGREDIENTS_RE.sub(self.sub_ingredients, line)
                    if not (line.startswith('{') or line.startswith('}')) and not '&' in line:
                        line = r'\multicolumn{2}{l}{%s}\\' % line.strip(r'\\')
                line = FRAC_RE.sub(self.sub_frac, line)
                
                #Apply changes
                lines[i] = line
        else:
            level = 0
            in_ingredients = False
            for i, line in enumerate(lines):
                #Apply some regex replace: unit, tabular organization in ingredients and frac
                if in_ingredients == False:
                    if line.startswith(r'<div id="ingredients">'):
                        in_ingredients = True
                elif in_ingredients == True:
                    if line.startswith('</div>'):
                        in_ingredients = False
                    else:
                        #line = UNITS_RE.sub(self.sub_units_html, line)
                        line = INGREDIENTS_HTML_RE.sub(self.sub_ingredients_html, line)
                line = FRAC_RE.sub(self.sub_frac_html, line)
                
                #Apply changes
                lines[i] = line

        if md.output_format == 'xcookybooky':
            write(r'')
            write(r'\end{recipe}')
        else:
            if has_meta_key(md, 'hint'):
                write(r'')
                write(r'<div id="hint">')
                write(r'<p>Astuce</p>')
                write(md.Meta['hint'][0])
                write(r'</div>')
            write('</body>')
            write('</html>')
        
        if md.output_format == 'xcookybooky':
            #Adjust text indentation
            for i, line in enumerate(lines):
                if line.startswith('[') or line.startswith('{') \
                or (line.startswith(r'\begin{') and not lines[i+1].startswith('[')):
                    line = ' ' * level * md.tab_length + line
                    level += 1
                elif line.startswith(']') or line.startswith('}') or line.startswith(r'\end{'):
                    level -= 1
                    line = ' ' * level * md.tab_length  + line
                else:
                    line = ' ' * level * md.tab_length  + line
        else:
            level = 0
            for i, line in enumerate(lines):
                if line.startswith('</'):
                    level -= 1
                    line = ' ' * level * md.tab_length  + line
                elif line.startswith('<') \
                and not ' />' in line and not '</' in line \
                and not line.startswith('<li') \
                and not line.startswith('<img') \
                and not line.startswith('<!'):
                    line = ' ' * level * md.tab_length + line
                    level += 1
                else:
                    line = ' ' * level * md.tab_length  + line
                    
                #Apply changes
                lines[i] = line
                
        return '\n'.join(lines)
