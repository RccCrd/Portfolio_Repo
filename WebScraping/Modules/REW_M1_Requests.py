#####Import Python Packages#####
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
#################################




def get_controlled_link(link):
    if link[:4] != 'http':
        link = 'https://www.immobiliare.it' + link
    return link


def request_and_append_links(asset_number, city_name, session):
    '''
    The function gets the links to the relevant pages on the immobiliare.it website, 
    taking in consideration the city of interest, and the amount of assets requested
    by the user. It returns a list of links of immobiliare.it website.

    
    Parameters
    ----------
    session : {'requests.sessions.Session'}
        The session variable is equal to a "requests.Session()" statement.

    city_name : {str}
        It is the name of the city that the scraping will be executed on.
    asset_number : {str}
        It is the number of assets that will be included in the scraping. The number 
        may not exceed 2000. 

    Returns
    ----------
    links : {list}
        It is a python list, containing the links found in the immobiliare.it pages 
        that refer to a certain city, stored in the parameter "city_name". Iterating
        through the links list is equivalent to iterating through the list of links 
        which refer to the assets found in the research (and which will be, ideally
        equal to the amount set in the asset_number variable). 


    
    '''


    links = []
    index = 1

    url = 'https://www.immobiliare.it/vendita-case/' + city_name.lower() + '/?criterio=rilevanza&pag='


    while len(links) < asset_number:
        content = session.get(url + str(index))
        index += 1
        soup = BeautifulSoup(content.text, 'lxml')
        div_tags = soup.find_all("div", {'class': "nd-mediaObject__content in-card__content in-realEstateListCard__content"})
        for tag in div_tags:
            a_tags = tag.find_all("a")
            for tag in a_tags:
                link = get_controlled_link(tag['href'])
                links.append(link)
        if not div_tags:
            break
    links = links[:asset_number]
    return links

def main():
     session = requests.Session()
     output_name,city_name,asset_number='output','Roma',123
     links=request_and_append_links(asset_number, city_name, session)
     print(f'the type of the "asset_number" variable is {type(links)}')

if __name__ == '__main__':
    main()