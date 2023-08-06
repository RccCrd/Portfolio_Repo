#####Import Python Packages#####
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re
#################################


#########Import Modules##########
from Modules import REW_M0_Get_input
from Modules import REW_M1_Requests
from Modules import REW_M2_Scrape_data
from Modules import REW_M3_Clean_data
from Modules import REW_M4_Write_data
#################################


def main():
    ##############MODULE 0 - REW_M0_Get_input ###################
    output_name,city_name,asset_number,research_type=REW_M0_Get_input.get_user_input()
    
    ##############MODULE 1 - REW_M1_Requests ###################
    session = requests.Session()
    neighborhoods = REW_M1_Requests.get_neighborhoods(asset_number, city_name, session , research_type)
    links = REW_M1_Requests.request_and_append_links(asset_number, city_name, session , neighborhoods)
    if not links:
        print('No links found. Exiting.')
        return
    ############MODULE 2 - REW_M2_Scrape_data ##################
    data = REW_M2_Scrape_data.scrape_data(links, session)
    if data.empty:
        print('No data scraped. Exiting.')
        return
    ############MODULE 3 - REW_M4_Write_data# ##################
    data = REW_M3_Clean_data.clean_data(data, city_name)
    ############MODULE 4 - REW_M4_Write_data# ##################
    REW_M4_Write_data.write_output_tocsv(data , output_name)
    print('Data successfully scraped and saved.')
    
if __name__ == '__main__':
    main()
