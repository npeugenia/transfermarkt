import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class TransfermarktScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://www.transfermarkt.fr'

    def get_top_players(self, base_url, total_pages=20):
        all_players_data = []
        
        for page in range(1, total_pages + 1):
            
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}/plus/?ajax=yw1&page={page}"
            
            print(f"\nScraping page {page}/{total_pages}")
            
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Erreur de requête HTTP avec le code {response.status_code} pour la page {page}")
                continue
            
            soup = BeautifulSoup(response.content, 'html.parser')
            players = soup.select('table.items > tbody > tr')

            for player in players:
                try:
                    
                    player_info = player.select_one('td table.inline-table')
                    if not player_info:
                        continue

                    name = player_info.select_one('td.hauptlink a').text.strip()
                    player_url = self.base_url + player_info.select_one('td.hauptlink a')['href']
                    position = player_info.select('tr')[1].td.text.strip()
                    
                    
                    club_img = player.select_one('td.zentriert img.tiny_wappen')
                    club = club_img['alt'] if club_img else "Club inconnu"
                    
                    value_element = player.select_one('td.rechts.hauptlink a')
                    value = value_element.text.strip() if value_element else "Non spécifié"
                    
                    
                    player_details = self.get_player_details(player_url)
                    
                    
                    player_data = {
                        'name': name,
                        'position': position,
                        'club': club,
                        'value': value,
                        'profile_url': player_url,
                        **player_details
                    }
                    
                    all_players_data.append(player_data)
                    print(f"Données récupérées pour {name}")
                    
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Erreur lors de la récupération des données: {str(e)}")
                    continue
            
            
            print(f"Page {page} terminée. Pause avant la prochaine page...")
            time.sleep(5)
                
        return all_players_data

    def get_player_details(self, player_url):
        print(f"Récupération des détails pour: {player_url}")
        response = requests.get(player_url, headers=self.headers)
        if response.status_code != 200:
            return {}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        details = {}
        
        try:
            
            info_table = soup.select_one('div.info-table')
            if info_table:
                info_rows = info_table.find_all('span', class_='info-table__content')
                for i in range(0, len(info_rows), 2):
                    if i + 1 < len(info_rows):
                        label = info_rows[i].text.strip().replace(':', '').lower().replace(' ', '_')
                        value = info_rows[i + 1].text.strip()
                        details[label] = value

            
            market_value = soup.select_one('div.tm-market-value-development-graph-small .current-value')
            if market_value:
                details['market_value'] = market_value.text.strip()

            
            birth_date = soup.select_one('span.info-table__content:-soup-contains("Date of birth")')
            if birth_date:
                birth_value = birth_date.find_next('span', class_='info-table__content--bold')
                if birth_value:
                    details['birth_date'] = birth_value.text.strip()

            
            nationality = soup.select_one('span.info-table__content:-soup-contains("Citizenship")')
            if nationality:
                nat_value = nationality.find_next('span', class_='info-table__content--bold')
                if nat_value:
                    details['nationality'] = nat_value.text.strip()

            
            contract = soup.select_one('span.info-table__content:-soup-contains("Contract expires")')
            if contract:
                contract_value = contract.find_next('span', class_='info-table__content--bold')
                if contract_value:
                    details['contract_expires'] = contract_value.text.strip()

        except Exception as e:
            print(f"Erreur lors de l'extraction des détails: {str(e)}")
            
        return details

def main():
    scraper = TransfermarktScraper()
    base_url = 'https://www.transfermarkt.fr/spieler-statistik/wertvollstespieler/marktwertetop'
    
    
    players_data = scraper.get_top_players(base_url, total_pages=20)
    
    if not players_data:
        print("Aucune donnée n'a été récupérée")
        return
    
    
    df = pd.DataFrame(players_data)
    
    
    df.to_csv('transfermarkt_players.csv', index=False, encoding='utf-8')
    print(f"Données sauvegardées dans transfermarkt_players.csv ({len(df)} joueurs)")
    
    
    df.to_json('transfermarkt_players.json', orient='records', force_ascii=False, indent=4)
    print(f"Données sauvegardées dans transfermarkt_players.json ({len(df)} joueurs)")

if __name__ == "__main__":
    main()