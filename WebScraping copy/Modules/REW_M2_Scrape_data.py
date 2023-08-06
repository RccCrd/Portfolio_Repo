#####Import Python Packages#####
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
#################################
def scrape_data(links, session):


    '''
    Parameters
    ----------
    session : {'requests.sessions.Session'}
        The session variable is equal to a "requests.Session()" statement.

    links : {list}
        It is a python list, containing the links found in the immobiliare.it pages 
        that refer to a certain city, stored in the parameter "city_name". Iterating
        through the links list is equivalent to iterating through the list of links 
        which refer to the assets found in the research (and which will be, ideally
        equal to the amount set in the asset_number variable). 

    Returns  
    ----------
    data  : {Pandas.Dataframe}
         It is a Pandas Dataframe containin the following fields, as extracted from each url:
         'posting_title': It is the title that the immobiliare.it website gave to the posting.
         'price': It is the price of the real estate asset as posted on immobiliare.it
         'rooms': It is the number of rooms published on immobiliare.it 
         'sqm': It is the number of square meters that make up the real estate asset published on immobiliare.it 
         'toilets': It is the number of toilets published on immobiliare.it 
         'floor': It is the floor number of the real estate asset as published on immobiliare.it 
         'link': It is the URL of the real estate asset on immobiliare.it 
         'location': It is the neighborhood where the real estate asset is localized 
    
    '''
    data = pd.DataFrame(columns=['posting_title', 'price', 'rooms', 'sqm', 'toilets', 'floor', 'link', 'location', 'tipologie'])

    for count, url_found in enumerate(tqdm(links, desc="Scraping Progress")):
        try:
            url , neighborhood_name = url_found
            real_estate = session.get(url)
            soup = BeautifulSoup(real_estate.text, 'lxml')

            div_tag = soup.find("h1", {'class': "in-titleBlock__title"})
            posting_title = div_tag.text if div_tag else 'na'
            try:
                div_tag = soup.find("li", {'class': "nd-list__item in-feat__item in-feat__item--main in-detail__mainFeaturesPrice"}) 
                if "€" in div_tag.text:           
                    price = div_tag.text.split('€')[1].strip() if div_tag else 'na'
                else:
                    price = 'na'
            except:
                div_tag = soup.find("li", {'class': "nd-list__item in-feat__item in-feat__item--main in-detail__mainFeaturesPrice in-detail__mainFeaturesPrice--interactive"}) 
                if "€" in div_tag.text:           
                    price = div_tag.text.split('€')[1].strip() if div_tag else 'na'
                else:
                    price = 'na'

            div_tag = soup.find("li", {'aria-label': "locali"})
            rooms = div_tag.text if div_tag else 'na'
   
            div_tag = soup.find("li", {'aria-label': "tipologie"})
            tipologie = div_tag.text if div_tag else 'na'

            div_tag = soup.find("li", {'aria-label': "piano"})
            print(div_tag)
            floor = div_tag.text if div_tag else 'na'

            div_tag = soup.find("li", {'aria-label': "superficie"})
            sqm = div_tag.text if div_tag else 'na'

            div_tag = soup.find("li", {'aria-label': 'bagni'}) or soup.find("li", {'aria-label': 'bagno'})
            toilets = div_tag.text if div_tag else 'na'


            location = neighborhood_name

            data.loc[count + 1] = [posting_title, price, rooms, sqm, toilets, floor, url, location, tipologie]

        except Exception as e:
            print(f'Error scraping {url_found}: {str(e)}')

    return data

def main():
    pass

if __name__ == '__main__':
    main()