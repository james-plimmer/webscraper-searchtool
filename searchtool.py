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
    # define the stopwords
    stopwords = [
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your',
        'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it',
        "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this',
        'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
        'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
        'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
        'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
        "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't",
        'doesn', "doesn't" ] 
    # intialise the frontier with the first page
    frontier = ['https://quotes.toscrape.com/']
    # keep track of pages visited
    visited = []
    
    # intialise the index
    index = {}
    
    # while there are pages to visit
    while frontier:
        # get the next page to visit (front of frontier)
        page = frontier.pop(0)
        print(f"Visiting {page}")
        # mark the page as visited
        visited.append(page)
        
        response = requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # scrape the page, tokenising all non-stopwords and counting their frequency on the page
        text = soup.get_text() # includes <title> and <meta> tags !!!
        # decode unicode characters
        text.encode().decode('unicode_escape')
        # only keelp alnums 
        text = ''.join([ c for c in text if c.isalnum() or c.isspace() ])
        words = [ w for w in text.lower().split() if w not in stopwords ]
        
        
        for w in words:
            # check if word already in index
            if w in index:
                # check if page already in index for that word
                if page in index[w]:
                    # increment word counter for that page
                    index[w][page] += 1
                else:
                    # add page to index for that word
                    index[w][page] = 1
            else:
                
                # add word to index with 1 count for current page
                index[w] = {page: 1}
        
        
        # find all links on the page
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
                # print(f"Adding {full_link} to frontier")
        
        # wait at least 6 seconds before making the request
        time.sleep(6.5)
        
    # save the index to a file
    # with open('index.json', 'w') as f:
    #     json.dump(index, f)


def main():
    while True:
        print("\n\n\n-----------------------------")
        print("build")
        print("load")
        print("-----------------------------")
        choice = input("Enter one of the above commands, or Q to quit: ")
        
        if choice.lower() == 'q':
            print("Goodbye!")
            break
        
        elif choice.lower() == 'build':
            build()
            print("Index built successfully.")
            continue
        
        elif choice.lower() == 'load':
            with open('index.json', 'r') as f:
                index = json.load(f)
            print("Index loaded successfully.")
            print(index['mountain'])
            continue
    
    
if __name__ == '__main__':
    main()
    




