#coding: utf-8

import gtk
import webkit
import settings
import json
import requests

class popup:
    def __init__(self, url):
        r = requests.get(url)
        if 200 == r.status_code:
            dados = r.content
            dados = json.loads(dados)
            
            titulo = 'Não Definido'
            descricao = 'Não Definido'
            categoria = 'Não Definido'
            curtidas = 'Não Definido'

            if 'name' in dados:
                titulo = dados['name']
            if 'description' in dados:
                descricao = dados['description']
            if 'category' in dados:
                categoria = dados['category']
            if 'likes' in dados:
                curtidas = dados['likes']
        else:
            print 'URL inválida'
            return

        conteudo = open('./HTML/descricaoTitulo.html', 'r').read()
        conteudo = conteudo.replace('{titulo}', titulo)
        conteudo = conteudo.replace('{descricao}', descricao)
        conteudo = conteudo.replace('{categoria}', categoria)
        conteudo = conteudo.replace('{curtidas}', str(curtidas))

        self.view = webkit.WebView() 

        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.set_title(titulo)
        self.win.set_size_request(400, 390)
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.set_resizable(False)
        color = gtk.gdk.color_parse('#fff')
        self.win.modify_bg(gtk.STATE_NORMAL, color)

        vbox = gtk.VBox(False, 1)

        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scrolledwindow.add(self.view)

        vbox.pack_end(scrolledwindow, True, True, 0)

        self.win.add(vbox)
        self.win.show_all()

        self.view.load_html_string(conteudo, settings.URL_BASE)
