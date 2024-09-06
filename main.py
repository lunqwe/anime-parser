import time
from utils import DataScrapper


def main():
    data = []
    scrapper = DataScrapper()
    links = scrapper.parse_anime_links()
    error_links = []
    for link in links:
        try:
            data.append(scrapper.get_anime_info(link))
            print(link)
        except ConnectionError:
            error_links.append(link)
            print(f'Error scrapping data from link: {link}. Added to retry list.')
            time.sleep(20) # preventing 429 Too Many Requests error
        except (ValueError, AttributeError):
            print(f'Parsing error at {link}. Link would be skipped.')
    
    print('starting rescrap...')
    for link in error_links:
        try:
            data.append(scrapper.get_anime_info(link))
        except ConnectionError:
            print(f'Failed scrapping data from link: {link}. This link would be skipped.')
    
    return data

print(main())
