import json
import requests
import argparse
import os
from datetime import datetime as dt

def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{file_path}'.")
        return None

class ScraperASC():
    def __init__(self,usr,pwd,dest) -> None:
        self.usr = usr
        self.pwd = pwd
        self.save_path = dest
        self.athletes = []
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,it-IT;q=0.8,it;q=0.7,es;q=0.6',
            'content-type': 'application/json',
            'origin': 'https://asc.tesseramento.app',
            'priority': 'u=1, i',
            'referer': 'https://asc.tesseramento.app/',}
        
        self.urls = {
            "login": "https://api.asc.tesseramento.app/api/services/user/login",
            "asd_info": "https://api.asc.tesseramento.app/api/services/user/me",
            "athletes": "https://api.asc.tesseramento.app/api/services/subscriber/all/lite/filtered",
            "card_download": "https://api.asc.tesseramento.app/api/services/card/pdf"
        }
        pass
    
    def get_me(self):
        """Load ASD info
        """
        response = requests.get(self.urls["asd_info"], headers=self.headers)
        if response.status_code == 200:
            print(f"Hello {response.json()['structureName']}")
        else:
            print("Failed loading ASD info")
        
    def login_to_asc(self):
        """Login with username and password to save the token
        """
        
        print({"username":self.usr, "password":self.pwd})
        response = requests.post(self.urls["login"],json={"username":self.usr, "password":self.pwd},headers=self.headers)
    
        if response.status_code == 200:
            print(f"Login successul")
            self.headers["Authorization"] = response.headers["Authorization"]
            self.get_me()
        else:
            print("Login failed!")
    
    def load_athletes(self):
        """Load atheletes 
        """
        response = requests.post(self.urls["athletes"], headers=self.headers, json = {"year": "2024"})
        if response.status_code == 200:
            print("Loaded athletes...")
            for athlete in response.json()['list']:
                print(f'{athlete["firstname"]} {athlete["lastname"]} {athlete["cardCode"]}')
                self.athletes.append(athlete)
        else:
            print("Failed loading ASD athetes")

    def dump_cards(self):
        for ath in self.athletes:
            self._download_file(f'{ath["lastname"]}_{ath["firstname"]}',ath['idSubscriber'],ath['fkCard'])
    
    def _download_file(self,athlete, id_athlete, id_card):
        print(f'Downloading card for {athlete}')
        url = f"{self.urls['card_download']}/{id_athlete}/{id_card}"
        response = requests.get(url, headers=self.headers)
        os.makedirs(self.save_path,exist_ok=True)
        
        if response.status_code == 200:
            if os.path.exists(f"{self.save_path}/{athlete}.pdf"):
                os.remove(f"{self.save_path}/{athlete}.pdf")
            with open(f"{self.save_path}/{athlete}.pdf", 'wb') as f:
                f.write(response.content)
            print(f"File downloaded successfully: {self.save_path}/{athlete}.pdf")
        else:
            print("Failed to download file")

def main():
    parser = argparse.ArgumentParser(
                    prog='ASC Card Scaper',
                    description='Scrapes ASC athletes cards from the website')
    parser.add_argument('-u','--user', help='ASC username', required=True)
    parser.add_argument('-p','--password', help='ASC password', required=True)
    parser.add_argument('-d','--destination', help='Cards pdf will be dumped here', required=True)
    parser.add_argument('-y','--year', help='Download this years` cards', default=dt.now().year)

    args = parser.parse_args()
    print(f"ASC Card Scraper started - scraping cards for {args.year}")
    
    scraper = ScraperASC(args.user,args.password,args.destination)
    scraper.login_to_asc()
    
    scraper.load_athletes()
    
    scraper.dump_cards()
    
    print("DONE.")
    
    pass

if __name__ == "__main__":
    main()