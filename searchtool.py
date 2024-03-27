import requests
from bs4 import BeautifulSoup
import json
import time
from unidecode import unidecode

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
        # replace unicode characters with ascii where possible
        soup = unidecode(str(soup))
        soup = BeautifulSoup(soup, 'html.parser')
        
        # scrape the page, tokenising all non-stopwords and counting their frequency on the page
        
        text = soup.get_text() # includes <title> and <meta> tags !!!
        # decode unicode characters
        text.encode().decode('unicode_escape')
        # only keelp alnums > 2 characters
        text = ''.join([ c for c in text if c.isalnum() or c.isspace() ])
        words = [ w for w in text.lower().split() if w not in stopwords and len(w) > 2]
        
        for posting in words:
            # check if posting already in index
            if posting in index:
                # check if pointer already in index for that posting
                if page in index[posting]:
                    # increment posting counter for that pointer
                    index[posting][page] += 1
                else:
                    # add pointer to index for that posting
                    index[posting][page] = 1
            else:
                print(posting)
                # add posting to index with 1 count for current pointer
                index[posting] = {page: 1}
        
        
        # find all links on the page
        for link in soup.find_all('a'):
            
            # only keep links on the quotes.toscrape.com domain
            if 'https://www.' in link.get('href'):
                continue
            
            full_link = "https://quotes.toscrape.com" + link.get('href')
            # append link to frontier if it has not been visited already and is not already in the frontier
            # only if it is on the quotes.toscrape.com domain
            if full_link not in visited and full_link not in frontier:
                frontier.append(full_link)
        
        # wait at least 6 seconds before making the request
        time.sleep(6.5)
        
    # save the index to a file
    with open('index.json', 'w') as f:
        json.dump(index, f)


def main():
    index = None
    
    while True:
        # give user time to read previous output
        time.sleep(1)
        # print the menu
        print("\n\n\n-----------------------------")
        print("build")
        print("load")
        print("print <query>")
        print("find <query> [query2] [query3] ...") 
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
            continue
        
        
        elif choice.split(' ')[0].lower() == 'print' and len(choice.split(' ')) == 2:
            # ensure index is loaded
            if index is None:
                print("Index not loaded.")
                continue
            
            query = choice.split(' ')[1]
            print(f"Searching for: {query}")
            # search the index for the query
            if query in index:
                print(f"Found {len(index[query])} results:")
                for page, count in index[query].items():
                    print(f"{page} - {count} occurences")
            else:
                print("No results found.")
        
        
        elif choice.split(' ')[0].lower() == 'find' and len(choice.split(' ')) > 1:
            # ensure index is loaded
            if index is None:
                print("Index not loaded.")
                continue
            
            query = choice.split(' ')[1:]
            print(f"Searching for: {' '.join(query)}")
            # search the index for the query
            
            # get the pointers for the first query
            pointers = index.get(query[0]).copy()
            
            # if there are more search terms
            if len(query) > 1:
                # for each subsequent query, get the pointers and add the count for each pointer if found and remove it if not
                for q in query[1:]:
                    ps = index.get(q)
                    for p in ps:
                        if p in pointers:
                            pointers[p] += ps[p]
                        
                
                # otherwise remove pointers that have not had their count increased
                p_to_remove = []
                for p in pointers:
                    if pointers[p] == index.get(query[0]).get(p):
                        p_to_remove.append(p)
                
                for p in p_to_remove:
                    del pointers[p]
            
            # if there are no pointers, no results found
            if not pointers:
                print("No results found.")
                continue
            
            print(f"Found {len(pointers)} results:")
            # sort the pointers by count
            pointers = {k: v for k, v in sorted(pointers.items(), key=lambda item: item[1], reverse=True)}
            for pointer in pointers:
                print(pointer)

        else:
            print("Invalid command.")
            continue
            
    
    
if __name__ == '__main__':
    main()
    




