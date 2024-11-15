import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class YoungTalentsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.base_url = 'https://www.transfermarkt.com'

    def get_young_talents(self, base_url, total_pages=20):
        all_players_data = []
        
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
                    
                    
                    position_element = player.select('td')[1]
                    position = position_element.text.strip() if position_element else "Unknown"
                    
                    
                    age_element = player.select('td')[3]
                    age = age_element.text.strip() if age_element else "Unknown"
                    
                    
                    club_element = player.select_one('td img.tiny_wappen')
                    club = club_element['alt'] if club_element else "Unknown club"
                    
                    
                    value_element = player.select_one('td.rechts.hauptlink')
                    value = value_element.text.strip() if value_element else "Not specified"
                    
                    
                    player_details = self.get_player_details(player_url)
                    
                    
                    player_data = {
                        'name': name,
                        'age': age,
                        'position': position,
                        'club': club,
                        'market_value': value,
                        'profile_url': player_url,
                        **player_details
                    }
                    
                    all_players_data.append(player_data)
                    print(f"Data retrieved for {name}")
                    
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error while retrieving data: {str(e)}")
                    continue
            
            
            print(f"Page {page} completed. Pausing before next page...")
            time.sleep(5)
                
        return all_players_data

    def get_player_details(self, player_url):
        print(f"Getting details for: {player_url}")
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

            
            nationality = soup.select_one('span.info-table__content:-soup-contains("Citizenship")')
            if nationality:
                nat_value = nationality.find_next('span', class_='info-table__content--bold')
                if nat_value:
                    details['nationality'] = nat_value.text.strip()

            
            birth_date = soup.select_one('span.info-table__content:-soup-contains("Date of birth")')
            if birth_date:
                birth_value = birth_date.find_next('span', class_='info-table__content--bold')
                if birth_value:
                    details['birth_date'] = birth_value.text.strip()

            
            foot = soup.select_one('span.info-table__content:-soup-contains("Foot")')
            if foot:
                foot_value = foot.find_next('span', class_='info-table__content--bold')
                if foot_value:
                    details['preferred_foot'] = foot_value.text.strip()

            
            height = soup.select_one('span.info-table__content:-soup-contains("Height")')
            if height:
                height_value = height.find_next('span', class_='info-table__content--bold')
                if height_value:
                    details['height'] = height_value.text.strip()

            
            youth_club = soup.select_one('span.info-table__content:-soup-contains("Youth clubs")')
            if youth_club:
                youth_value = youth_club.find_next('span', class_='info-table__content--bold')
                if youth_value:
                    details['youth_clubs'] = youth_value.text.strip()

        except Exception as e:
            print(f"Error while extracting details: {str(e)}")
            
        return details

def main():
    scraper = YoungTalentsScraper()
    base_url = 'https://www.transfermarkt.com/spieler-statistik/wertvollstespieler/marktwertetop/plus/0/galerie/0?ausrichtung=alle&spielerposition_id=alle&altersklasse=u21&jahrgang=0&land_id=0&kontinent_id=0&yt0=Anzeigen'
    
    
    players_data = scraper.get_young_talents(base_url, total_pages=20)
    
    if not players_data:
        print("No data retrieved")
        return
    
    
    df = pd.DataFrame(players_data)
    
   
    df.to_csv('transfermarkt_young_talents.csv', index=False, encoding='utf-8')
    print(f"Data saved in transfermarkt_young_talents.csv ({len(df)} players)")
    
    
    df.to_json('transfermarkt_young_talents.json', orient='records', force_ascii=False, indent=4)
    print(f"Data saved in transfermarkt_young_talents.json ({len(df)} players)")

if __name__ == "__main__":
    main() 