import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.action_chains import ActionChains


class DataScrapper:
    def __init__(self) -> None:
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36z'
        }
        self.KEYS_TO_FORMAT = ['Жанры:', 'Темы:', 'Тема:']
        self.KEY_TRANSLATOR = {
            'Тип:': 'Type',
            'Эпизоды:': 'Episodes amount',
            'Длительность эпизода:': 'Episode duration',
            'Статус:': 'Status',
            'Жанры:': 'Genres',
            'Темы:': 'Topics',
            'Тема:': 'Topic',
            'Рейтинг:': 'Age restrictions',
            'Альтернативные названия:': "Alternative names",
            'Лицензировано:': 'Licensed',
        }
        options = FirefoxOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)

    def load_soup(self, url: str) -> BeautifulSoup:
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
        else:
            raise ConnectionError(
                f'Error while connecting to website: {response.status_code} - {response.reason}')

    def get_additional_info(self, soup: BeautifulSoup) -> dict:
        result = {}
        additional_data = soup.select_one('div.b-entry-info')
        for data in additional_data.select('div.line-container')[:7]:
            key = data.select_one('div.key').get_text(' ')
            value = data.select_one('div.value')
            if key == 'Статус:':
                # spliting anime status and its release date
                status = value.select_one('span.b-anime_status_tag')['data-text']
                dates = value.select_one('span.b-tooltipped')
                value = f'{status} - {dates}'

            elif key in self.KEYS_TO_FORMAT:
                # getting the necessary additional data
                value = [x.text for x in value.select('span.genre-ru')]

            else:
                value = value.get_text(' ')
            display_key = self.KEY_TRANSLATOR.get(key)
            if display_key:
                result[display_key] = value
        return result

    def get_screenshots(self, url):
        lst = []
        soup = self.load_soup(url)
        screenshots = soup.select('a.c-screenshot')
        for screenshot in screenshots:
            lst.append(screenshot['href'])
        return lst

    def get_anime_info(self, url):
        result = {}
        soup = self.load_soup(url)
        try:
            title_data = soup.select_one('h1').text
            title, original_title = title_data.split(' / ')
            result['Title'] = title
            result['Original title'] = original_title

            additional_data = self.get_additional_info(soup)
            result = result | additional_data

            description = soup.select_one('div.b-text_with_paragraphs').text
            rating = soup.select_one('div.score-value').text
            result['Description'] = description
            result['Rating'] = rating
            resources_url = soup.select_one('div.resources-loader')['data-postloaded-url']
            screenshots = self.get_screenshots(resources_url)
            result['Screenshots'] = screenshots
        except AttributeError as e:
            raise AttributeError(f'AttributeError: {e}')
        except ValueError as e:
            raise ValueError(f'ValueError: {e}')
            
        return result
    
    def scroll_to_bottom(self, max_scrolls=100, scroll_pause_time=0.2, scroll_step=350):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scrolls = 0
        current_position = 0

        while scrolls < max_scrolls:
            next_position = min(current_position + scroll_step, last_height)
            self.driver.execute_script(f"window.scrollTo({{top: {next_position}, behavior: 'smooth'}});")
            time.sleep(scroll_pause_time)
            current_position = next_position
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height and current_position >= last_height:
                break
            
            last_height = new_height
            scrolls += 1

        return scrolls
    
    def parse_anime_links(self):
        links_list = []
        for page_num in range(1, 1087):
            link = f'https://shikimori.one/animes/page/{page_num}'
            self.driver.get(link)
            self.scroll_to_bottom()
            links = self.driver.find_elements(By.CLASS_NAME, "cover.anime-tooltip-processed")
            for anime_link in links:
                if anime_link not in links_list:
                    links_list.append(anime_link.get_attribute('href'))
        self.driver.close()
        return links_list

            
