#####Import Python Packages#####
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
#################################

''' 
   Parameters  
    ----------
    data  : {Pandas.Dataframe}
         It is a Pandas Dataframe containing the following fields, as extracted from each url:
         'posting_title': It is the title that the immobiliare.it website gave to the posting.
         'price': It is the price of the real estate asset as posted on immobiliare.it
         'rooms': It is the number of rooms published on immobiliare.it 
         'sqm': It is the number of square meters that make up the real estate asset published 
          on immobiliare.it 
         'toilets': It is the number of toilets published on immobiliare.it 
         'floor': It is the floor number of the real estate asset as published on immobiliare.it 
         'link': It is the URL of the real estate asset on immobiliare.it 
         'location': It is the neighborhood where the real estate asset is localized 
    city_name : {str}
            It is the name of the city that the scraping will be executed on.

    Returns
    ----------
    data  : {Pandas.Dataframe}
        It is the same Dataframe as the one received as input in the paramentes, but with formatting
         and cleaning applied to the Data
        

'''


def clean_data( data, city_name):
    # Clean text formatting (only numbers)
    pd.options.display.float_format = '{:,.2f}'.format

    #data['price'] = data['price'].apply(lambda x: x.replace(".", ""))
    data = data[data['tipologie'] == 'na']
    data.loc[:, 'price'] = data['price'].str.split('-').str[0]
    data['city'] = city_name
    data["price"] = data["price"].apply(lambda x: re.sub("[^0-9,]", "", x))
    data.loc[:,"price"] = pd.to_numeric(data["price"], errors="coerce")
    data.loc[:,"sqm"] = data["sqm"].apply(lambda x: re.sub("[^0-9,]", "", x))
    data.loc[:,"sqm"] = pd.to_numeric(data["sqm"], errors="coerce")
    # Create a counting column for quantifying the assets for each location
    data['count'] = 1
    print('test')

def main():
    pass

if __name__ == '__main__':
    main()