#!/usr/bin/env python
#coding: utf-8

#author: Mateus Ferreira Silva
#author: Arthur Assuncao

import gtk 
import webkit
import settings
import re
import requests
import os
import popupTitulo


class spto:
    def __init__(self):
        self.buscaAtual = '' # armazena o conteúdo pesquisado atualmente
        
        self.view = webkit.WebView() 
        self.view.connect('navigation-requested', self.on_click_link)

        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.win.set_title('SPTO - Sistema de Pesquisa de Títulos Online')
        self.win.set_size_request(800, 600)
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.win.set_resizable(False)

        vbox = gtk.VBox(False, 2)
        hbox = gtk.HBox()
        
        # Barra de menu
        menuBar = gtk.MenuBar()
        menuArquivo = gtk.Menu()
        arquivo = gtk.MenuItem('Arquivo')
        arquivo.set_submenu(menuArquivo)

        limparPesquisa = gtk.MenuItem('Limpar Pesquisa')
        limparPesquisa.connect('activate', self.limparWebView)
        menuArquivo.append(limparPesquisa)

        limparCache = gtk.MenuItem('Limpar Cache')
        limparCache.connect('activate', self.limparCache)
        menuArquivo.append(limparCache)

        sep = gtk.SeparatorMenuItem()
        menuArquivo.append(sep)
        
        sair = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        sair.connect('activate', gtk.main_quit)
        menuArquivo.append(sair)

        menuCreditos = gtk.Menu()
        sobre = gtk.MenuItem('Sobre')
        sobre.set_submenu(menuCreditos)
        sobre.connect('activate', self.sobre)
        menuBar.append(arquivo)
        menuBar.append(sobre)
        vbox.pack_start(menuBar, False, False, 0)

        # Campo de busca
        labelTitulo = gtk.Label('Título:')
        self.campoBuscar = gtk.Entry()
        self.campoBuscar.connect('activate', self.buscar)
        btBuscar = gtk.Button('Buscar')
        btBuscar.connect("clicked", self.buscar)
        btBuscar.set_size_request(80, 25)
        hbox.pack_start(labelTitulo, False, False, 5)
        hbox.pack_start(self.campoBuscar, True, True, 0)
        hbox.pack_start(btBuscar, False, False, 1)

        # Barra de Rolagem na webView
        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)
        scrolledwindow.add(self.view)

        # Adicionar hbox e scrolledwindow
        vbox.pack_start(hbox, False, False, 0)
        vbox.pack_end(scrolledwindow, True, True, 0)

        self.win.add(vbox)
        self.win.connect("destroy", gtk.main_quit) # Fechar ao clicar
        self.win.show_all()

    def on_click_link(self, view, frame, req, data=None):
        '''
        Listener para links. 
        Toda vez que um link é clicado no webView, ele é chamado.
        '''

        uri = req.get_uri()
        if uri.startswith("file:///"):
            self.buscar(None)
            return False
        elif uri.startswith("program:/"):
            print uri.split("/")[1]
        else: 
            print uri
            popupTitulo.popup(uri)
        return True

    def limparCache(self, view):
        for raiz, diretorios, arquivos in os.walk('./cache'):
            for arquivo in arquivos:
                if arquivo.endswith('.html'):
                    os.remove(os.path.join(raiz, arquivo))

    def limparWebView(self, view):
        self.view.load_html_string('', settings.URL_BASE)
        self.buscaAtual = ''

    def sobre(self, view):
        sobre = open('./HTML/sobre.html', 'r').read() 
        self.view.load_html_string(sobre, settings.URL_BASE)
        self.buscaAtual = ''

    def buscar(self, button):
        busca = self.campoBuscar.get_text().strip()

        if len(busca) == 0:
            pass
        elif self.buscaAtual == busca:
            pass
        elif self.verifica_cache(busca.lower()) != None:
            self.buscaAtual = busca
            self.view.load_html_string(self.verifica_cache(busca.lower()), settings.URL_BASE)
        else:
            print 'Realizando pesquisa para "{}"'.format(busca)
            self.buscaAtual = busca
            # Recebimento da resposta de busca
            resposta, conteudo = self.busca(busca)
            if resposta == 200:
                conteudo = self.estrutura_resultado(conteudo)
            elif resposta == 404:
                conteudo = self.estrutura_resultado(None)
            open('./cache/{}.html'.format(busca.lower()), 'w').write(conteudo)
            print 'Criando arquivo de cache "{}.html"'.format(busca.lower())
            self.view.load_html_string(conteudo, settings.URL_BASE)

    def verifica_cache(self, arquivo):
        try:
            conteudo = open('./cache/{}.html'.format(arquivo.lower())).read()
            return conteudo
        except IOError as e:
            return None

    def estrutura_resultado(self, filmes):
        if filmes == None:
            conteudo = open('./HTML/naoEncontrado.html', 'r').read() 
            return conteudo
        else:
            conteudo = open('./HTML/titulos.html', 'r').read() 
            lista = []
            for filme in filmes['filmes']:
                item = '<a href="http://graph.facebook.com/http://www.imdb.com{url}"><li class="well well-small titulo"><img src="{img}" height="44" width="32" /><span>{titulo}</span></li></a>'.format(
                    img=filme['imagem'], url=filme['link'], titulo=filme['titulo'])
                lista.append(item)
            texto_conteudo = '<br>'.join(lista)
            conteudo = conteudo % texto_conteudo
            return conteudo

    def retorna_lista(self, url):
        html = requests.get(url).content
        itens = re.findall(r'<td class="primary_photo">.*?<img.*?src="(.+?)".*?></a> </td>.*?<td class="result_text"> <a href="(.+?)".*?>(.+?)</td>', html)
        filmes = {'filmes' : []}
        if len(itens) > 0:
            for img, link, titulo in itens: 
                titulo = re.sub('<small>.+?</small>', '',titulo) # Remove tag small
                titulo = re.sub('<[^>]*>', '', titulo) # Remove tags e seus conteúdos
                if not re.match(r'/name/nm.+?', link): # Somente Titles
                   filme = {'titulo' : titulo, 'link' : link, 'imagem' : img}
                   filmes['filmes'].append(filme)
            resposta = 200
        else:
            resposta = 404
        return resposta, filmes

    def gera_url(self, pesquisa):
        pesquisa = pesquisa.strip()
        pesquisa = pesquisa.replace(' ', '+')
        if len(pesquisa) > 0:
            return 'http://www.imdb.com/find?q={0}'.format(pesquisa)
        else:
            return None
            
    def busca(self, texto):
      url = self.gera_url(texto)
      return self.retorna_lista(url)

if __name__ == "__main__":
    spto()
    gtk.main()
