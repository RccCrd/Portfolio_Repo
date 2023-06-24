import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import re


def get_controlled_link(link):
    if link[:4] != 'http':
        link = 'https://www.immobiliare.it' + link
    return link


def request_and_append_links(asset_number, city_name, session):
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


def scrape_data(links, session):
    data = pd.DataFrame(columns=['posting_title', 'price', 'rooms', 'sqm', 'toilets', 'floor', 'link', 'location', 'tipologie'])

    for count, url_found in enumerate(tqdm(links, desc="Scraping Progress")):
        try:
            real_estate = session.get(url_found)
            soup = BeautifulSoup(real_estate.text, 'lxml')

            div_tag = soup.find("h1", {'class': "in-titleBlock__title"})
            posting_title = div_tag.text if div_tag else 'na'

            div_tag = soup.find("li", {'class': "nd-list__item in-feat__item in-feat__item--main in-detail__mainFeaturesPrice"})
            if isinstance(div_tag, (int, float)):
                price = div_tag.text.split('€')[1].strip() if div_tag else 'na'
            else:
                price = 'na'

            div_tag = soup.find("li", {'aria-label': "locali"})
            rooms = div_tag.text if div_tag else 'na'

            div_tag = soup.find("li", {'aria-label': "tipologie"})
            tipologie = div_tag.text if div_tag else 'na'

            div_tag = soup.find("div", {'class': "in-feat__data"})
            floor = div_tag.text if div_tag else 'na'

            div_tag = soup.find("li", {'aria-label': "superficie"})
            sqm = div_tag.text if div_tag else 'na'

            div_tag = soup.find("li", {'aria-label': 'bagni'}) or soup.find("li", {'aria-label': 'bagno'})
            toilets = div_tag.text if div_tag else 'na'

            div_tag = soup.find("div", {'class': "in-titleBlock"})
            location_string = div_tag.text
            location_area = div_tag.find_all("span", {'class': "in-location"})
            location_area = location_area[1]
            location = location_area.text if div_tag else 'na'

            data.loc[count + 1] = [posting_title, price, rooms, sqm, toilets, floor, url_found, location, tipologie]

        except Exception as e:
            print(f'Error scraping {url_found}: {str(e)}')

    return data


def clean_data(data):
    # Clean text formatting (only numbers)
    pd.options.display.float_format = '{:,.2f}'.format

    data['price']
def create_output(output_name, data, city_name):
    # Clean text formatting (only numbers)
    pd.options.display.float_format = '{:,.2f}'.format

    data['price'] = data['price'].apply(lambda x: x.replace(".", ""))
    data = data[data['tipologie'] == 'na']
    data['price'] = data['price'].str.split('-').str[0]
    data.loc[:, 'city'] = city_name
    data["price"] = data["price"].apply(lambda x: re.sub("[^0-9,]", "", x))
    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data["sqm"] = data["sqm"].apply(lambda x: re.sub("[^0-9,]", "", x))
    data["sqm"] = pd.to_numeric(data["sqm"], errors="coerce")
    # Create a counting column for quantifying the assets for each location
    data['count'] = 1
    data.to_csv(output_name, sep=",", header=True, index=False)


def main():
    ## Getting User Input##
    #The User Input is:
    #output_name: The name (excluding the extension name) of the output file. The output will be stored by default in the active folder.
    #city_name: It is the name of the city that the scraping will be executed on.
    #asset_number: It is the number of assets that will be included in the scraping. The number may not exceed 2000. 
    output_name = input('Please enter the output filename (for example "Output"):') + '.csv'
    city_name = input('Please enter the city of interest (in local language, for example: "Napoli"):')

    asset_number = int(input('Please enter the number of RE Assets to analyze (min 1 - max 2000):'))
    if asset_number > 2000:
        print('The chosen amount exceeds the maximum admitted value, defaulting to 2000.')
        asset_number = 2000
    if asset_number < 1:
        print('The chosen amount is lower than the minimum admitted value, defaulting to 1.')
        asset_number = 1
    session = requests.Session()

    links = request_and_append_links(asset_number, city_name, session)

    if not links:
        print('No links found. Exiting.')
        return

    data = scrape_data(links, session)

    if data.empty:
        print('No data scraped. Exiting.')
        return

    create_output(output_name, data, city_name)

    print('Data successfully scraped and saved.')


if __name__ == '__main__':
    main()
