import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class YoungPlayerStatsScraper:
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
            players = soup.select('table.items > tbody > tr:not(.thead)')

            for player in players:
                try:
                    
                    name_element = player.select_one('td.hauptlink a')
                    if not name_element:
                        continue

                    name = name_element.text.strip()
                    player_url = self.base_url + name_element['href']
                    
                    
                    columns = player.select('td')
                    position = columns[1].text.strip() if len(columns) > 1 else "Unknown"
                    age = columns[3].text.strip() if len(columns) > 3 else "Unknown"
                    
                    
                    club_element = player.select_one('td img.tiny_wappen')
                    if club_element:
                        club = club_element['alt']
                    else:
                        club_element = player.select_one('td a[href*="/verein/"]')
                        club = club_element.text.strip() if club_element else "Unknown club"
                    
                   
                    value_element = player.select_one('td.rechts.hauptlink')
                    value = value_element.text.strip() if value_element else "Not specified"
                    
                    
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
                    
                    
                    if name and position and age:
                        player_data = {
                            'name': name,
                            'position': position,
                            'club': club,
                            'market_value': value,
                            'profile_url': player_url,
                            'age': age,
                            **stats
                        }
                        all_players_stats.append(player_data)
                    print(f"Stats retrieved for {name}")
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error while retrieving stats: {str(e)}")
                    continue
            
            print(f"Page {page} completed. Pausing before next page...")
            time.sleep(5)
                
        return all_players_stats

    def get_detailed_stats(self, player_url):
        """Récupère les statistiques détaillées par compétition"""
        print(f"Getting detailed stats for: {player_url}")
        
        
        stats_url = player_url.replace('/profil/', '/leistungsdatendetails/')
        
        response = requests.get(stats_url, headers=self.headers)
        if response.status_code != 200:
            return {}
        
        soup = BeautifulSoup(response.content, 'html.parser')
        stats_by_competition = {}
        
        try:
            
            stats_table = soup.select('table.items > tbody > tr:not(.bg_grey)')
            
            for row in stats_table:
                columns = row.select('td')
                if len(columns) < 13:
                    continue
                
                competition = columns[2].text.strip()
                stats_by_competition[competition] = {
                    'matches': columns[3].text.strip(),
                    'goals': columns[4].text.strip(),
                    'assists': columns[5].text.strip(),
                    'minutes_played': columns[6].text.strip(),
                    'yellow_cards': columns[7].text.strip(),
                    'second_yellows': columns[8].text.strip(),
                    'red_cards': columns[9].text.strip(),
                    'goals_conceded': columns[10].text.strip() if columns[10].text.strip() != '-' else '0',
                    'clean_sheets': columns[11].text.strip() if columns[11].text.strip() != '-' else '0'
                }
                
        except Exception as e:
            print(f"Error while extracting detailed stats: {str(e)}")
            
        return stats_by_competition

def main():
    scraper = YoungPlayerStatsScraper()
    base_url = 'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop?land_id=0&ausrichtung=alle&spielerposition_id=alle&altersklasse=u21&jahrgang=0&kontinent_id=0&plus=1'
    
    
    players_stats = scraper.get_players_stats(base_url, total_pages=20)
    
    if not players_stats:
        print("No stats retrieved")
        return
    
    
    df = pd.DataFrame(players_stats)
    
    
    df.to_csv('young_players_stats.csv', index=False, encoding='utf-8')
    print(f"Stats saved in young_players_stats.csv ({len(df)} players)")
    
    
    df.to_json('young_players_stats.json', orient='records', force_ascii=False, indent=4)
    print(f"Stats saved in young_players_stats.json ({len(df)} players)")

if __name__ == "__main__":
    main()