#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import requests
from bs4 import BeautifulSoup
import math
import re
import os


def compiler_fichier_csv(data, categorie):
    entete = ["product_page_url", "universal_ product_code (upc)", "title",
              "price_including_tax", "price_excluding_tax", "number_available", "product_description",
              "category", "review_rating", "image_url"]

    with open('resultat_scrapping_'+categorie+'.csv', 'w', encoding="utf-8", newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(entete)
        for row in data:
            writer.writerow(row)

def telecharger_images(data):
    if not os.path.exists(os.path.join(current_directory, "images")):
        os.mkdir(os.path.join(current_directory, "images"))
    directory_travail = os.path.join(current_directory, "images")
    for row in data:
        nom_fichier = row[0].split('/')[4]
        response = requests.get(row[9]).content
        with open(directory_travail+"\\"+nom_fichier+".jpg", "wb+") as file:
            file.write(response)



url = "http://books.toscrape.com/catalogue/category/books_1/index.html"
urls_a_scrapper = []
current_directory = os.getcwd()
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.text, features="html.parser")
    urls = soup.find('div', class_="side_categories").findAll('a')
    for url in urls:
        urls_a_scrapper.append(["http://books.toscrape.com/catalogue/category"+url['href'][2:], url.text.strip()])

for url_categorie in urls_a_scrapper[1:]:
    # scrap le nombre de livres et les urls de tous les livres
    urls_livres = []
    urls=[url_categorie[0]]
    data_csv = []
    livres = []
    categorie = url_categorie[1]
    response = requests.get(url_categorie[0])
    if response.ok:
        # recherche le nombre de livres. Pour rappel 20 livres par page
        soup = BeautifulSoup(response.text, features="html.parser")
        pagination = soup.find("form").findAll("strong")
        for nombre_de_livres in pagination:
            livres.append(nombre_de_livres.text)
        if math.ceil(int(livres[0])/20) > 1:
            # met a jour la liste urls
            liste_url = url_categorie[0].split('/')[:-1]
            url_pagination = ("/").join(liste_url)
            i = 2
            while i <= math.ceil(int(livres[0])/20):
                urls.append(url_pagination+"/page-"
                            + str(i)+".html")
                i = i + 1
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
            data_livre = []
            if response.ok:
                #product_page_url
                data_livre.append(url_livre)
                soup = BeautifulSoup(response.content, features="html.parser")
                tds = soup.findAll('td')
                #universal_ product_code (upc)
                data_livre.append(tds[0].text)
                title = soup.find('h1')
                #title
                data_livre.append(title.text)
                #price_including_tax
                data_livre.append(tds[3].text)
                #price_excluding_tax
                data_livre.append(tds[2].text)
                #number_available
                livres_disponibles = re.findall("\d+", tds[5].text)
                data_livre.append(livres_disponibles[0])
                #product_description
                description = soup.find(class_="product_page").findAll('p')
                data_livre.append(description[3].text)
                #category
                data_livre.append(categorie)
                #review_rating
                data_livre.append(tds[6].text)
                #image_url
                image_img = soup.find(class_="carousel").find('img')
                data_livre.append("http://books.toscrape.com" + image_img['src'][5:])
                data_csv.append(data_livre)

    compiler_fichier_csv(data_csv, categorie)
    telecharger_images(data_csv)
