import requests
from bs4 import BeautifulSoup
import json
import time
from unidecode import unidecode

#TODO: store pointers as unique ids for each page, not the full url. Check teams for requirements updates.

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
        
        # only keelp alnums > 2 characters, replacing punctuation with whitespace
        text = ''.join([ c if c.isalnum() else ' ' for c in text])
        words = [ w for w in text.lower().split() if w not in stopwords and len(w) > 2]
        
        # track the position of each word on the page in a dictionary
        word_pos =  {}
        for i, word in enumerate(words):
            if word in word_pos:
                word_pos[word].append(i)
            else:
                word_pos[word] = [i]
        
        for posting, pos in word_pos.items():
            # check if posting already in index
            if posting in index:
                # check if pointer already in index for that posting
                if page in index[posting]:
                    # increment posting occurance counter for that pointer by the number of positions
                    index[posting][page]['occurances'] += len(pos)
                    # add the positions of the posting on the page
                    index[posting][page]['positions'].extend(pos)
                else:
                    # add pointer to index for that posting and add the positions of the posting on the page
                    index[posting][page] = {'occurances': len(pos), 'positions': pos}
            else:
                print(posting)
                # add posting to index with count for current pointer
                index[posting] = {page: {'occurances': len(pos), 'positions': pos}}
        
        
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
        if index != None : print("print <query>\nfind <query> [query2] [query3] ...")
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
                print(f"Printing inverted index for {query}:")
                print(index.get(query))
            else:
                print("No results found.")
        
        
        elif choice.split(' ')[0].lower() == 'find' and len(choice.split(' ')) > 1:
            # ensure index is loaded
            if index is None:
                print("Index not loaded.")
                continue
            
            query = choice.split(' ')[1:]
            # remove trailing whitespace
            if query[-1] == '':
                query = query[:-1]
                
            print(f"\n\nSearching for: {' '.join(query)}")
            # search the index for the query
            
            consec_words = {}
            all_words = {}
            some_words = {}
            
            # look for each search term and add the page to lowest ranked list if found, tracking number of words for which the page is found
            for word in query:
                if word in index:
                    for page in index[word].keys():
                        if page not in some_words.keys():
                            # track the number of search terms found on the page, the first occurance of a search term on the page, and the total number of occurences of the search terms on the page
                            some_words[page] = {"nQueryTerms" : 1, "first" : index[word][page]['positions'][0], "total" : index[word][page]['occurances']}
                        else:
                            # increment the number of search terms found on the page, update the first occurance of the search a on the page if necessary, and increment the total number of occurences of the search terms on the page
                            some_words[page]['nQueryTerms'] += 1
                            if index[word][page]['positions'][0] < some_words[page]['first']:
                                some_words[page]['first'] = index[word][page]['positions'][0]
                            some_words[page]['total'] += index[word][page]['occurances']
            
            # if a page appears in all search terms, add to all words list
            for page in some_words.keys():
                if some_words[page]['nQueryTerms'] == len(query):
                    all_words[page] = some_words[page]
            
            # remove any pages that are in all_words from some_words
            for page in all_words.keys():
                some_words.pop(page)
                
            # detemine if search query is consecutive in pages found in all_words
            # get index of first word in query
            for page in all_words:
                for pos in index[query[0]][page]['positions']:
                    # check if the other words in the query are in the same order on the page
                    consec = True
                    for i in range(1, len(query)):
                        if pos + i not in index[query[i]][page]['positions']:
                            consec = False
                            break
                    if consec:
                        consec_words[page] = all_words[page]
                        break
            
            # remove any pages that are in consec_words from all_words
            for page in consec_words.keys():
                all_words.pop(page)
                    
            # sort consecutive words by number of occurences then by earliest occurence
            consec_words = {k: v for k, v in sorted(consec_words.items(), key=lambda item: (-item[1]['total'], item[1]['first']))}
            # sort all words by number of occurences then by earliest occurence
            all_words = {k: v for k, v in sorted(all_words.items(), key=lambda item: (-item[1]['total'], item[1]['first']))}
            # sort some words by number of search terms then number of occurences then by earliest occurence
            some_words = {k: v for k, v in sorted(some_words.items(), key=lambda item: (-item[1]['nQueryTerms'], -item[1]['total'], item[1]['first']))}
            
            
            # if there are no pointers, no results found
            if not some_words and not all_words and not consec_words:
                print("No results found.")
                continue
            
            
            print("Results are ranked by number of search terms present, then the number of occurences of any search terms, then earliest occurence of a search term.")
            # first print pages with the search term in consecutive order
            print(f"\n\nFound {len(consec_words.keys())} Pages with Exact Query Match:")
            for page, sorting_info in consec_words.items():
                print(page, "--- Number of Search Terms:", sorting_info['nQueryTerms'], "- Total Occurences of Search Terms:", sorting_info['total'], "- First Occurence of Search Term:", sorting_info['first'])
                
            # then print pages with all search terms in any order
            print(f"\n\nFound {len(all_words.keys())} Pages with All Query Terms:")
            for page, sorting_info in all_words.items():
                print(page, "--- Number of Search Terms:", sorting_info['nQueryTerms'], "- Total Occurences of Search Terms:", sorting_info['total'], "- First Occurence of Search Term:", sorting_info['first'])


            # then print pages with some search terms in any order
            print(f"\n\nFound {len(some_words.keys())} Pages with Some Query Terms:")
            for page, sorting_info in some_words.items():
                print(page, "--- Number of Search Terms:", sorting_info['nQueryTerms'], "- Total Occurences of Search Terms:", sorting_info['total'], "- First Occurence of Search Term:", sorting_info['first'])


            
        else:
            print("Invalid command.")
            continue
            
    
    
if __name__ == '__main__':
    main()