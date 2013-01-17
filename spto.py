#coding: utf-8

import re
import threading
import time
import urllib2

def exibe_lista(url):
    html = urllib2.urlopen(url).read()
    itens = re.findall(r'<td class="primary_photo">.*?<img.*?src="(.+?)".*?></a> </td>.*?<td class="result_text"> <a href="(.+?)".*?>(.+?)</td>', html)
    if len(itens) > 0:
        for img, link, item in itens:
            item = re.sub('<small>.+?</small>', '',item) # Remove tag small
            item = re.sub('<[^>]*>', '', item) # Remove tags e seus conteúdos
            if not re.match(r'/name/nm.+?', link): # Somente Titles
                print 'TÍTULO: {0}\nLINK: {1}\nIMAGEM: {2}\n'.format(item, link, img)
    else:
        print 'Nenhum resultado encontrado'

def gera_url(pesquisa):
    pesquisa = pesquisa.strip()
    pesquisa = pesquisa.replace(' ', '+')
    if len(pesquisa) > 0:
        return 'http://www.imdb.com/find?q={0}'.format(pesquisa)
    else:
        return None

if __name__ == "__main__":
    pesquisa = raw_input('Buscar: ')
    url = gera_url(pesquisa)
    if url:
        exibe_lista(url)
    else:
        print 'Campo de Busca vazio'
    