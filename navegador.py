import gtk 
import webkit 
import thread
import gobject
import spto
import json
import settings

def estrutura_resultado(filmes):
    conteudo = open('titulos.html', 'r').read()
    lista = []
    for filme in filmes['filmes']:
        item = '<li class="well well-small titulo"><img src="{img}" height="44" width="32" /><span>{titulo}</span></li>'.format(img=filme['imagem'], url=filme['link'], titulo=filme['titulo'])
        lista.append(item)
    
    texto_conteudo = '<br>'.join(lista)
    conteudo = conteudo % texto_conteudo
    return conteudo

view = webkit.WebView() 

win = gtk.Window(gtk.WINDOW_TOPLEVEL)
win.width = 500
win.height = 300

view = webkit.WebView()

resposta, conteudo = spto.busca('lord of the rings')
#resposta, conteudo = spto.busca('sempre ao seu lado')
if resposta == 200:
    conteudo = estrutura_resultado(conteudo)
elif resposta == 404:
    conteudo = 'Nenhum resultado encontrado'

view.load_html_string(conteudo, settings.URL_BASE)

win.add(view)
win.show_all()

gtk.main()