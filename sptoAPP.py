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
        self.buscaAtual = '' # armazena o conteúdo pesquisado atualmente
        self.view = webkit.WebView() 
        self.view.connect("navigation-requested", self.on_click_link)
        win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        win.set_title('SPTO - Sistema de Pesquisa de Títulos Online')
        win.set_size_request(800, 600)
        win.set_position(gtk.WIN_POS_CENTER)
        win.set_resizable(False)

        vbox = gtk.VBox(False, 2)
        hbox = gtk.HBox()
        
        # Barra de menu
        menuBar = gtk.MenuBar()
        menuArquivo = gtk.Menu()
        arquivo = gtk.MenuItem("Arquivo")
        arquivo.set_submenu(menuArquivo)
        
        sair = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        sair.connect("activate", gtk.main_quit)
        menuArquivo.append(sair)

        menuCreditos = gtk.Menu()
        creditos = gtk.MenuItem("Créditos")
        creditos.set_submenu(menuCreditos)
        menuBar.append(arquivo)
        menuBar.append(creditos)
        vbox.pack_start(menuBar, False, False, 0)

        # Campo de busca
        labelTitulo = gtk.Label('Título:')
        self.campoBuscar = gtk.Entry()
        self.campoBuscar.connect("activate", self.buscar)
        btBuscar = gtk.Button('Buscar')
        btBuscar.connect("clicked", self.buscar)
        btBuscar.set_size_request(80, 25)
        hbox.pack_start(labelTitulo, False, False, 5)
        hbox.pack_start(self.campoBuscar, True, True, 0)
        hbox.pack_start(btBuscar, False, False, 1)

        # Barra de Rolagem na webView
        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        textview = gtk.TextView()
        scrolledwindow.add(self.view)

        # Adicionar hbox e scrolledwindow
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_end(scrolledwindow, True, True, 0)

        win.add(vbox)
        win.connect("destroy", gtk.main_quit) # Fechar ao clicar
        win.show_all()

    def on_click_link(self, view, frame, req, data=None):
        """Describes what to do when a href link is clicked"""

        # As Ryan Paul stated he likes to use the prefix program:/ if the
        # link is being used like a button, the else will catch true links
        # and open them in the webbrowser
        uri = req.get_uri()
        if uri.startswith("file:///"):
            self.buscar(None)
            return False
        elif uri.startswith("program:/"):
            print uri.split("/")[1]
        else: 
            print uri
        return True

    def buscar(self, button):
        busca = self.campoBuscar.get_text()
        if len(busca) == 0 or self.buscaAtual == busca:
            pass
        else:
            print 'Realizando pesquisa para "{}"'.format(busca)
            self.buscaAtual = busca
            # Recebimento da resposta de busca
            resposta, conteudo = spto.busca(busca)
            if resposta == 200:
                conteudo = self.estrutura_resultado(conteudo)
            elif resposta == 404:
                conteudo = self.estrutura_resultado(None)
            self.view.load_html_string(conteudo, settings.URL_BASE)

    def estrutura_resultado(self, filmes):
        if filmes == None:
            conteudo = open('naoEncontrado.html', 'r').read() 
            return conteudo
        else:
            conteudo = open('titulos.html', 'r').read() 
            lista = []
            for filme in filmes['filmes']:
                item = '<a href="http://graph.facebook.com/http://www.imdb.com{url}"><li class="well well-small titulo"><img src="{img}" height="44" width="32" /><span>{titulo}</span></li></a>'.format(
                    img=filme['imagem'], url=filme['link'], titulo=filme['titulo'])
                lista.append(item)
            texto_conteudo = '<br>'.join(lista)
            conteudo = conteudo % texto_conteudo
            return conteudo

if __name__ == "__main__":
    sptoAPP()
    gtk.main()