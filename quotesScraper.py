import requests
from bs4 import BeautifulSoup
from collections import defaultdict

all_qoutes = []
tagged_quotes = defaultdict(list)

def __sources():
    URL = "http://quotes.toscrape.com/"
    sources =[URL]
    for i in range(2,11):
        sources.append(URL + f"page/{str(i)}/")
    return sources

def __get_html(URL):
    result = requests.get(URL)
    return result.text

def __parse_quotes(page):
    soup = BeautifulSoup(page, 'html.parser')
    quotes = soup.find_all('div', class_="quote")

    for quote in quotes:
        text = quote.find('span', class_ = "text").text
        author = quote.find("small", class_="author").text
        all_qoutes.append([text, author])
        try:
            tags = quote.find("a", class_="tag")
            for tag in tags:
                tagged_quotes[tag].append([text, author])
        except:
            pass
    

def quotes_main():
    all_sources = __sources()
    for source in all_sources:
        __parse_quotes(__get_html(source))
    return (all_qoutes, tagged_quotes)

if __name__ == "__main__":
    print("\nSources\n","\n".join(__sources()))
    print("All qoutes before", all_qoutes)
    print("Tagged quotes before", tagged_quotes)
    print(quotes_main())
    
