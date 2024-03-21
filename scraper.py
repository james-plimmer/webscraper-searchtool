import requests
from bs4 import BeautifulSoup
import json

def scrape_page(page):
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.select('div.quote')   
    
    results = []
    for quote in quotes:
        text = quote.find('span', class_='text').text.strip()
        author = quote.find('small', class_='author').text.strip()
        author_link = base_link + quote.find('a')['href']
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        

        results.append({
            'text': text,
            'author': author,
            'author_link': author_link,
            'tags': tags
        })
    return results, soup

base_link = 'https://quotes.toscrape.com'
quote_index = []
page = base_link
while page:
    results, soup = scrape_page(page)
    quote_index.extend(results)
    next_button = soup.find('li', class_='next')
    if next_button:
        page = base_link + next_button.find('a')['href']
    else:
        page = None

with open('index.json', 'w') as f:
    json.dump(quote_index, f)
    




