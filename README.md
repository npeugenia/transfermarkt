# transfermarkt
Scrapping Python Project for data usage 
Description du Projet
Ce projet consiste en la collecte et l'analyse de données à partir du site Transfermarkt.fr. Grâce au web scraping, j'ai extrait des données relatives aux performances des joueurs, à leurs valeurs marchandes et à divers autres indicateurs. Ces informations ont été utilisées pour effectuer des analyses et générer des visualisations graphiques qui mettent en lumière différents aspects des joueurs et du marché.

Objectifs
Collecter des données sur les joueurs de football depuis Transfermarkt.fr.
Analyser les performances et les valeurs marchandes des joueurs.
Créer des graphiques et des visualisations pour mieux interpréter les données et offrir des insights pertinents.
Fonctionnalités du Projet
Scraping des Données : Extraction des données des pages de joueurs sur Transfermarkt.fr en utilisant des scripts de scraping.
Nettoyage et Préparation : Traitement des données brutes pour les rendre exploitables, suppression des doublons, gestion des valeurs manquantes, etc.
Analyse des Données : Analyse statistique des performances, calculs des valeurs moyennes, comparaison de divers indicateurs.
Visualisations Graphiques : Création de graphiques interactifs et statiques pour représenter les données de manière claire et intuitive (valeurs marchandes, performances comparatives, etc.).

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class MostValuablePlayersScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://www.transfermarkt.com'

    def get_players_stats(self, base_url, total_pages=20):
        all_players_stats = []
        
        for page in range(1, total_pages + 1):
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}&page={page}"
            
            print(f"\nScraping page {page}/{total_pages}")
            
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"HTTP request error with code {response.status_code} for page {page}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            players = soup.select('table.items > tbody > tr[class*="odd"], table.items > tbody > tr[class*="even"]')
          
                    stats = {
                        'matches': columns[4].text.strip() if len(columns) > 4 else "0",
                        'goals': columns[5].text.strip() if len(columns) > 5 else "0",
                        'assists': columns[6].text.strip() if len(columns) > 6 else "0",
                        'yellow_cards': columns[7].text.strip() if len(columns) > 7 else "0",
                        'second_yellows': columns[8].text.strip() if len(columns) > 8 else "0",
                        'red_cards': columns[9].text.strip() if len(columns) > 9 else "0",
                        'minutes_played': columns[10].text.strip() if len(columns) > 10 else "0",
                        'goals_conceded': columns[11].text.strip() if len(columns) > 11 else "0",
                        'clean_sheets': columns[12].text.strip() if len(columns) > 12 else "0"
                    }
