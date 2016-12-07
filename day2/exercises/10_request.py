# -*- coding: utf-8 -*-

import urllib2
# Un petit utilitaire fait maison pour écrire un CSV avec des Dictionaires et Unicode
from goodiebag.writer import UnicodeWriter
# Si BeautifulSoup n'est pas installé: pip install beautifulsoup4
from bs4 import BeautifulSoup

base = "https://www.leboncoin.fr/velos/offres/ile_de_france/paris/?location=Paris&o="
ads = []

def clean(string):
    return string.strip().replace('\n', ' ').replace('\r', ' ')

def save_ad(soup):
    # On stock plusieurs valeurs dans un dictionaire nommé "values" et on ajoute
    values = {
        'title':       clean(soup.select('h1')[0].text),
        'description': clean(soup.select('.line.properties_description')[0].text),
        'price':       clean(soup.select('.item_price .value')[0].text),
        'city':        clean(soup.select('.line_city .value')[0].text)
    }
    # On a ajoute cette annonce à la liste des annonces à sauvegarder
    ads.append(values)

def fetch_ad(url):
    # On ouvre l'autre URL et on stock le resultat dans body
    body = urllib2.urlopen(url).read()
    # Parse le HTML avec Beautiful Soup
    save_ad( BeautifulSoup(body, 'html.parser') )

def fetch_list(page = 1):
    # On ouvre l'autre URL et on stock le resultat dans body
    body = urllib2.urlopen(base + str(page)).read()
    # Parse le HTML avec Beautiful Soup
    soup = BeautifulSoup(body, 'html.parser')
    # Tous les éléments de la liste
    for list_item in soup.select(".list_item"):
        # Seulement les annonces avec un prix
        if list_item.section.h3 != None:
            url = list_item['href']
            # L'URL sur Le Bon Coin ne contient pas le protocol
            url = url if url.startswith("http") else "http:%s" % url
            # On affiche dans la console la procédure en cours
            print u"Téléchargement de %s" % url
            # On appelle ici l'autre fonction pour télécharger une annonce
            fetch_ad(url)
            break

# Toutes les annonces de la page 1 sont stockées dans la liste "ads"
fetch_list(1)
# On affiche le resultat au format CSV
writer = UnicodeWriter(open("./ads.csv", 'w'), fieldnames=['title', 'price', 'city', 'description'])
# Ajoute toutes les lignes une par une
( writer.writerow(ad) for ad in ads  )
