import requests
from bs4 import BeautifulSoup
import json
import time

# def scrape_page(page, base_link):
#     response = requests.get(page)
#     print(datetime.datetime.now())
#     soup = BeautifulSoup(response.text, 'html.parser')
#     quotes = soup.select('div.quote')   
    
#     results = []
#     for quote in quotes:
#         text = quote.find('span', class_='text').text.strip()
#         author = quote.find('small', class_='author').text.strip()
#         author_link = base_link + quote.find('a')['href']
#         tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        

#         results.append({
#             'text': text,
#             'author': author,
#             'author_link': author_link,
#             'tags': tags
#         })
#     return results, soup

def build():
    # intialise the frontier with the first page
    frontier = ['https://quotes.toscrape.com/']
    # keep track of pages visited
    visited = []
    
    # intialise the index
    index = []
    
    # while there are pages to visit
    while frontier:
        # get the next page to visit (front of frontier)
        page = frontier.pop(0)
        print(f"Visiting {page}")
        # mark the page as visited
        visited.append(page)
        
        # find all links on the page
        response = requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            
            # only keep links on the quotes.toscrape.com domain
            if 'https://www.' in link.get('href'):
                continue
            
            full_link = "https://quotes.toscrape.com" + link.get('href')
            # print(full_link)
            # append link to frontier if it has not been visited already and is not already in the frontier
            # only if it is on the quotes.toscrape.com domain
            if full_link not in visited and full_link not in frontier:
                frontier.append(full_link)
                print(f"Adding {full_link} to frontier")
        
        # wait 6 seconds before making the request
        time.sleep(6.5)
        
    
    
    
    # base_link = 'https://quotes.toscrape.com'
    # quote_index = []
    # pages_visited = []
    # page = base_link
    # # while there is another page to crawl
    # while page:
    #     # scrape the page if it has not been visited already
    #     if page not in pages_visited:
    #         print(f"Scraping {page}")
    #         results, soup = scrape_page(page, base_link)
    #     else:
    #         continue
        
    #     pages_visited.append(page)
    #     quote_index.extend(results)
    #     # find the next button
    #     next_button = soup.find('li', class_='next')
    #     if next_button:
    #         page = base_link + next_button.find('a')['href']
    #     else:
    #         page = None

    # save the index to a file
    # with open('index.json', 'w') as f:
    #     json.dump(quote_index, f)


def main():
    while True:
        print("\n\n\n-----------------------------")
        print("build")
        print("-----------------------------")
        choice = input("Enter one of the above commands, or Q to quit: ")
        
        if choice.lower() == 'q':
            print("Goodbye!")
            break
        
        elif choice.lower() == 'build':
            build()
            print("Index built successfully.")
            continue
    
    
if __name__ == '__main__':
    main()
    




