# Anime Webscraper

## Description

Anime Webscraper is a Python-based project that implements a parser to extract and provide detailed information about anime. This tool scrapes data from popular anime encyclopedia website, offering users a comprehensive database of anime titles, descriptions, images, and more.

## Features

- Extracts anime information (in sites basic language) including:
  - Title 
  - Description
  - Cover image URL and additional media like screenshots etc.
  - Additional metadata (release year, genre, etc.)
- Sources data from shikimori.one, a leading anime encyclopedia


## Installation

```bash
git clone https://github.com/your-username/anime-webscraper.git
cd anime-webscraper
pip install -r requirements.txt
```

## Usage

```python
from utils import DataScrapper

scraper = DataScrapper()
anime_info = scraper.get_anime_info("https://shikimori.one/animes/37521-vinland-saga) # or any anime you want to get from shikimori.one
print(anime_info)
```
- Also there is a main.py file, which parsing the whole data about animes. In this case the parsing process takes a long time due to the large amount of data.

## Dependencies

- Python 3.7+
- Selenium
- BeautifulSoup4
- Requests

## Disclaimer

This tool is for educational purposes only. Please be respectful of the websites you are scraping and adhere to their robots.txt files and terms of service.

## Contact

For any queries or suggestions, please open an issue in the GitHub repository.
