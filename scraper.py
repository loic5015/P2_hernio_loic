import requests
from bs4 import BeautifulSoup
import math
import re

entete = ["product_page_url", "universal_ product_code (upc)", "title",
          "price_including_tax", "price_excluding_tax", "number_available", "product_description",
          "category", "review_rating", "image_url"]
data_csv = []
urls = ["http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"]

# scrap le nombre de livres et les urls de tous les livres
urls_livres = []
livres = []
categorie = "test"
response = requests.get(urls[0])
if response.ok:
    # recherche le nombre de livres. Pour rappel 20 livres par page
    soup = BeautifulSoup(response.text, features="html.parser")
    pagination = soup.find("form").findAll("strong")
    for nombre_de_livres in pagination:
        livres.append(nombre_de_livres.text)
    if math.ceil(int(livres[0])/20) > 1:
        # met a jour la liste urls
        urls.append("http://books.toscrape.com/catalogue/category/books/mystery_3/page-"+str(math.ceil(int(livres[0])/20))
                    +".html")

    # rechercher toutes les urls des livres sur toutes les pages de la categorie
    for url_pagines in urls:
        response = requests.get(url_pagines)
        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")
            a_balises = soup.find("ol").findAll("a")
            for a in a_balises:
                url_global = "http://books.toscrape.com/catalogue"+a["href"][8:]
                if url_global not in urls_livres:
                    urls_livres.append(url_global)

    #recherche des informations de la page details d'un livre pour completion d'une liste dans data_csv
    for url_livre in urls_livres:
        response = requests.get(url_livre)
        data_livre = {}
        data_livre["product_page_url"] = url_livre
        if response.ok:
            soup = BeautifulSoup(response.content, features="html.parser")
            tds = soup.findAll('td')
            data_livre["universal_ product_code"] = tds[0].text
            data_livre["price_including_tax"] = tds[3].text
            data_livre["price_excluding_tax"] = tds[2].text
            livres_disponibles = re.findall("\d+", tds[5].text)
            data_livre["number_available"] = livres_disponibles[0]
            data_livre["category"] = categorie
            data_livre["review_rating"] = tds[6].text
            title = soup.find('h1')
            data_livre["title"] = title.text
            description = soup.find(class_="product_page").findAll('p')
            data_livre["product_description"] = description[3].text
            image_img = soup.find(class_="carousel").find('img')
            data_livre["image_url"] = "'http://books.toscrape.com" + image_img['src'][5:]
        data_csv.append(data_livre)

print(livres)
print(data_csv)