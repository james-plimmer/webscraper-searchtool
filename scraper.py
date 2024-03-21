import requests
from bs4 import BeautifulSoup
import json

base_link = 'https://quotes.toscrape.com'
response = requests.get(base_link)
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

print(json.dumps(results))