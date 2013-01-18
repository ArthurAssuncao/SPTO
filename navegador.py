#coding: utf-8

import gtk 
import webkit 
import thread
import gobject
import spto
import json
import settings

class sptoAPP:
    def __init__(self):
        view = webkit.WebView() 
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_title('SPTO - Sistema de Pesquisa de Títulos Online')
        win.set_size_request(800, 600)
        win.set_position(gtk.WIN_POS_CENTER)

        vbox = gtk.VBox(False, 2)
        hbox = gtk.HBox()
        
        # Barra de menu -------------
        menuBar = gtk.MenuBar()
        menuArquivo = gtk.Menu()
        arquivo = gtk.MenuItem("Arquivo")
        arquivo.set_submenu(menuArquivo)
        menuCreditos = gtk.Menu()
        creditos = gtk.MenuItem("Créditos")
        creditos.set_submenu(menuCreditos)
        menuBar.append(arquivo)
        menuBar.append(creditos)
        vbox.pack_start(menuBar, False, False, 0)

        # Campo de busca
        labelTitulo = gtk.Label('Título:')
        campoBuscar = gtk.Entry()
        btBuscar = gtk.Button('Buscar')
        btBuscar.set_size_request(80, 25)
        hbox.pack_start(labelTitulo, False, False, 5)
        hbox.pack_start(campoBuscar, True, True, 0)
        hbox.pack_start(btBuscar, False, False, 1)

        # Recebimento da resposta de busca
        resposta, conteudo = spto.busca('Matrix')

        if resposta == 200:
            conteudo = self.estrutura_resultado(conteudo)
        elif resposta == 404:
            conteudo = 'Nenhum resultado encontrado'

        view.load_html_string(conteudo, settings.URL_BASE)

        # Barra de Rolagem
        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        textview = gtk.TextView()
        scrolledwindow.add(view)

        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_end(scrolledwindow, True, True, 0)

        win.add(vbox)
        win.connect("destroy", gtk.main_quit)
        win.show_all()

    def estrutura_resultado(self, filmes):
        conteudo = open('titulos.html', 'r').read() 
        lista = []
        for filme in filmes['filmes']:
            item = '<li class="well well-small titulo"><img src="{img}" height="44" width="32" /><span>{titulo}</span></li>'.format(img=filme['imagem'], url=filme['link'], titulo=filme['titulo'])
            lista.append(item)
        
        texto_conteudo = '<br>'.join(lista)
        conteudo = conteudo % texto_conteudo
        return conteudo

sptoAPP()
gtk.main()