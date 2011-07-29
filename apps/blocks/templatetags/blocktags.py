from django import template 
#import Library, Node, TemplateSyntaxError
from blocks.models import Block
from django.conf import settings

register = template.Library()

class Cmsblock(template.Node):

    def __init__(self, block_key, lang, block_as):
        #print block_key, lang, block_as
        if block_key:
            self.block_key = template.Variable(block_key)
        self.block_key_str = block_key[1:-1]
        if lang:
            self.lang = template.Variable(lang)
        self.lang_str = lang[1:-1]
        if block_as:
            self.block_as = template.Variable(block_as)
        self.block_as_str = block_as[1:-1]

    def render(self, context):
        try:
            block_key = self.block_key.resolve(context)
        except:
            block_key = self.block_key_str
        try:
            lang = self.lang.resolve(context)
        except:
            lang = self.lang_str
        try:
            block_as = self.block_as.resolve(context)
        except:
            block_as = self.block_as_str

        if lang not in settings.LANGUAGES:
            lang = lang.split('-')[0]
        res = Block.objects.filter_or_default(block_key=block_key, lang=lang)
        if res:
            if block_as:
                context[block_as] = template.Template(res[0].content).render(context)
                return ''
            else:
                return template.Template(res[0].content).render(context)
        else:
            return "<!-- el block '%s' '%s' no se pudo cargar -->" % (block_key, lang)


def do_render_block(parser, token):
    """
    Genera el html de un block desde el cms.
    con 1 argumento:
        render_block 'key_del_block'
    con 2 argumentos:
        render_block 'key_del_block' 'lang'
    con 4 argumentos:
        render_block 'key_del_block' 'lang' as 'nuevo_block'
    """
    block = token.split_contents()
    lang = ''
    block_as = ''
    if len(block) < 2:
        raise template.TemplateSyntaxError, '%s takes exactly at least one argument' % block[0]
    elif len(block) == 2:
        block_key = block[1]
    elif len(block) == 3:
        if block[2] == 'as':
            raise template.TemplateSyntaxError, '"as" incompleto'
        p, block_key, lang = block
    elif len(block) == 5:
        if block[3] != 'as':
            raise template.TemplateSyntaxError, "'as' incompleto. render_block 'nombre_del_block' 'lang' as 'nuevo_block'"
        p, block_key, lang, _as, block_as, = block
    else:
        raise template.TemplateSyntaxError, "'as' incompleto. render_block 'nombre_del_block' 'lang' as 'nuevo_block'"

    return Cmsblock(block_key, lang, block_as)

register.tag('render_block', do_render_block)
