import requests
from bs4 import BeautifulSoup
import math

entete = ["product_page_url", "universal_ product_code (upc)", "title",
          "price_including_tax", "price_excluding_tax", "number_available", "product_description",
          "category", "review_rating", "image_url"]

urls = ["http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"]
urls_livres = []
livres = []
response = requests.get(urls[0])
if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")
    pagination = soup.find("form").findAll("strong")
    for nombre_de_livres in pagination:
        livres.append(nombre_de_livres.text)
    if math.ceil(int(livres[0])/20) > 1:
        urls.append("http://books.toscrape.com/catalogue/category/books/mystery_3/page-"+str(math.ceil(int(livres[0])/20))
                    +".html")

    for url_pagines in urls:
        response = requests.get(url_pagines)
        if response.ok:
            soup = BeautifulSoup(response.text, features="html.parser")
            a_balises = soup.find("ol").findAll("a")
            for a in a_balises:
                url_global = "http://books.toscrape.com/catalogue"+a["href"][7:]
                if url_global not in urls_livres:
                    urls_livres.append(url_global)

print(urls_livres)

print(livres)