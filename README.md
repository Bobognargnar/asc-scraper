# ASC card scraper

Author: Fabrizio La Rosa

## Usage

* Install dependencies 

`python -m pip install -r requirements.txt`

* Launch program with your username and password

`python .\scraper.py --user <username> --password <password> --destination ./tessere`

* Compile it with pyInstaller


```
python -m pip install pyinstaller
python -m PyInstaller scraper.py --name asc_scraper --clean --distpath .\bin
```