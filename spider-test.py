import requests
from bs4 import BeautifulSoup


def get_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    #print all info in "a" tag
    #print(soup.find(id="vector-main-menu"))
    #var = soup.find('a')
    #print(soup.title.string)

    tag = soup.find_all("a")

    for t in tag:
        url2 = t.get("href")
        print(url2)

    #print(tag)

get_page(input("What url would you like to scrape? "))