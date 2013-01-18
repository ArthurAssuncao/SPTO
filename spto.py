#coding: utf-8

import re
import threading
import time
import urllib2

def retorna_lista(url):
    html = urllib2.urlopen(url).read()
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

def gera_url(pesquisa):
    pesquisa = pesquisa.strip()
    pesquisa = pesquisa.replace(' ', '+')
    if len(pesquisa) > 0:
        return 'http://www.imdb.com/find?q={0}'.format(pesquisa)
    else:
        return None
        
def busca(texto):
  url = gera_url(texto)
  return retorna_lista(url)

if __name__ == "__main__":
    pesquisa = raw_input('Buscar: ')
    url = gera_url(pesquisa)
    if url:
        retorna_lista(url)
    else:
        print 'Campo de Busca vazio'
    
