# Football Squad Builder

## Description
Le **Football Squad Builder** est un projet innovant qui combine web scraping, analyse de données et simulation dans Football Manager 2024 (FM24). 
L'objectif principal est d'explorer l'impact de la data dans la construction d'une équipe de football performante, en intégrant des joueurs sélectionnés sur la base de leur potentiel et de leur valeur de marché.

Ce projet inclut :
- **Scraping** des 500 joueurs les plus chers et les 500 jeunes les plus prometteurs (< 21 ans) depuis Transfermarkt.
- **Simulation** d'une saison complète dans FM24 avec un club personnalisé, en analysant les performances et ajustant les stratégies.
- **Développement** d'un site web permettant de générer une équipe en fonction d'un budget et d'une formation.

---

## Déroulement du projet

### Saison dans FM24
1. **Création du club et début de saison** : Avec une sélection initiale basée sur les données scrapées, notre équipe a démarré difficilement, se plaçant à la 18ème place en Premier League en janvier.
2. **Recrutement intelligent** : Grâce à nos données, nous avons renforcé l’équipe lors du mercato hivernal.
3. **Résultats** : Une remontée spectaculaire nous a permis de terminer 7ème, décrochant une place en Conference League.

### Développement Web
Nous travaillons actuellement sur un site web qui permettra aux utilisateurs de :
- Entrer un budget (en millions).
- Sélectionner une formation (ex : 4-3-3, 3-5-2, etc.).
- Générer une équipe optimisée selon les données scrapées.

---

## Fonctionnalités (Actuelles et Futures)
- **Scraping** : Extraction automatisée des données de Transfermarkt.
- **Simulation FM** : Analyse des performances des joueurs et des stratégies.
- **Génération d’équipes** : Création d’équipes optimisées selon des contraintes budgétaires et tactiques.
- **Interface web (en cours)** : Un site intuitif pour démocratiser l’utilisation des données dans le football.

---

## Aperçu du Code

Voici un extrait de notre script de scraping utilisé pour extraire les données :

```python
import requests
from bs4 import BeautifulSoup

def scrape_transfermarkt(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    players = []
    for player in soup.select('.spielerdaten'):
        name = player.select_one('.name').text.strip()
        value = player.select_one('.value').text.strip()
        players.append({'name': name, 'value': value})
    return players

# Exemple d'utilisation
url = "https://www.transfermarkt.fr/some-page"
data = scrape_transfermarkt(url)
print(f"Joueurs extraits : {len(data)}")
```

---

## Prochaines Étapes
- [x] Finaliser la structure de données pour le site web.
- [x] Continuer le développement de l'interface utilisateur.
- [x] Tester la génération d’équipes sur différents budgets et formations.
- [ ] Déployer le site web sur Vercel.

---

## Contact
Pour toute question ou suggestion, contactez-nous :  
**Nom** : Votre nom  
**Email** : votre.email@example.com  
**GitHub** : [Votre profil GitHub](https://github.com)

---

**Note** : Ce projet est en cours de développement actif. Des visuels et des mises à jour seront ajoutés au fur et à mesure.
