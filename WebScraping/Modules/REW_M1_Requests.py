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


def get_neighborhoods(asset_number, city_name, session , research_type):
    ''' 
    The function gets the links to the relevant pages on the 
    immobiliare.it website, taking in consideration the city of interest, 
    and scraping the pages that represent each neighborhood of which the
    relevant city is made of, according to the immobiliare.it website. 
    The output is a python list named 'neighborhoods'.
    session : {'requests.sessions.Session'}
    The session variable is equal to a "requests.Session()" statement.

    Parameters
    ----------

    asset_number : {str}
    It is the number of assets that will be included in the scraping. The number 
    may not exceed 2000. 
    
    city_name : {str}
    It is the name of the city that the scraping will be executed on.
    
    session : {'requests.sessions.Session'}
        The session variable is equal to a "requests.Session()" statement.

    research_type  : {str}
        It's a variable inputed by the user. It carries the information wether
        the user is interested in scraping the data related to a rent posting
        or a sale posting on the immobiliare.it website.
         
    Returns
    ----------

    neighborhoods : {list} 
    It is the output from the "get_neighborhoods" function, it is a python list 
    of touples containing  (href_value, neighborhood_name) i.e. respectively:
    1. The url of the immobiliare.it website connected to a certain neighborhood 
    the city stored in the city_name variable.
    2. The name of the neighborhood.
    The list is a collection of all the neighborhoods of which a city is made of
    according to the immobiliare.it website. The scraping function will use the 
    url of each neighborhood in order to make a research for all the available 
    postings, and label them as "located" in the neighborhood "neighborhood_name".

'''
    neighborhoods = []
    counter_neighborhoods = 0
    if research_type.lower() == 'sale':
        url = 'https://www.immobiliare.it/vendita-case/' + city_name.lower() + '/?criterio=rilevanza&pag='
    if  research_type.lower() == 'rent':
        url = 'https://www.immobiliare.it/affitto-case/' + city_name.lower() + '/?criterio=rilevanza&pag='
    content = session.get(url)
    soup = BeautifulSoup(content.text, 'lxml')
    div_tags = soup.find_all("li", {'class': "nd-stackItem"})
    
    for tag in div_tags:
        counter_neighborhoods = counter_neighborhoods + 1 
        href_value = tag.a['href']
        neighborhood_name = tag.text
        neighborhoods.append((href_value, neighborhood_name))

    return neighborhoods

def request_and_append_links(asset_number, city_name, session , neighborhoods):
    '''
    The function gets the links to the relevant pages on the immobiliare.it website, 
    taking in consideration the city of interest, all the neighborhoods of the city of interest, and the amount of assets requested
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

    neighborhoods : {list} 
        It is the output from the "get_neighborhoods" function, it is a python list 
        of touples containing  (href_value, neighborhood_name) i.e. respectively:
        1. The url of the immobiliare.it website connected to a certain neighborhood 
        the city stored in the city_name variable.
        2. The name of the neighborhood.
        The list is a collection of all the neighborhoods of which a city is made of
        according to the immobiliare.it website. The scraping function will use the 
        url of each neighborhood in order to make a research for all the available 
        postings, and label them as "located" in the neighborhood "neighborhood_name".

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


    # url = 'https://www.immobiliare.it/vendita-case/' + city_name.lower() + '/?criterio=rilevanza&pag='
    
    for link_neighborhood in neighborhoods:
        index = 1
        url , neighborhood_name = link_neighborhood
        while len(links) < asset_number:
            print (f'Getting URLs: {round(len(links)/asset_number*100 , 0)} %', end='\r')

            content = session.get(url +  '/?criterio=rilevanza&pag=' + str(index))
            index += 1
            soup = BeautifulSoup(content.text, 'lxml')
            div_tags = soup.find_all("div", {'class': "nd-mediaObject__content in-card__content in-realEstateListCard__content"})
            for tag in div_tags:
                a_tags = tag.find_all("a")
                for tag in a_tags:
                    link = get_controlled_link(tag['href'])
                    links.append((link , neighborhood_name))
            if not div_tags:
                break
        # print('no more links in ' , neighborhood_name , "arrived to " , len(links))
    links = links[:asset_number]
    return links

def main():
     session = requests.Session()
     output_name,city_name,asset_number='output','Roma',123
     links=request_and_append_links(asset_number, city_name, session)
     print(f'the type of the "asset_number" variable is {type(links)}')

if __name__ == '__main__':
    main()