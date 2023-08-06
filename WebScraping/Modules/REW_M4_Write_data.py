#####Import Python Packages#####
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
import os
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
    output_name : {str}
           The name (excluding the extension name) of the output file. The output will be stored by default in the active folder.
       

    Returns
    ----------
    None
        

'''

import os
import pandas as pd

def write_output_tocsv(data, output_name):
    # Validate the output_name parameter
    if not isinstance(output_name, str):
        raise ValueError("Output name must be a string.")

    # Create the output folder if it doesn't exist
    output_folder = 'Output'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Construct the output file path
    output_file = os.path.join(output_folder, output_name)

    try:
        # Write the DataFrame to a CSV file
        data.to_csv(output_file, sep=",", header=True, index=False)

        print("Data successfully written to", output_file)
    except Exception as e:
        print("Error occurred while writing data to CSV:", str(e))

def main():
    pass

if __name__ == '__main__':
    main()
