def get_user_input():
    '''
    The function gets user input from the console upon running.
    
        Parameters
        ----------
        No parameter is passed to the function (all input is user input from console)
    
        Returns
        ----------
        output_name : {str}
            The name (excluding the extension name) of the output file. The output will be stored by default in the active folder.
        city_name : {str}
            It is the name of the city that the scraping will be executed on.
        asset_number : {str}
            It is the number of assets that will be included in the scraping. The number may not exceed 2000. 
  
    '''
    output_name = input('Please enter the output filename (for example "Output"):') + '.csv'
    city_name = input('Please enter the city of interest (in local language, for example: "Napoli"):')
    asset_number = int(input('Please enter the number of RE Assets to analyze (min 1 - max 2000):'))
    if asset_number > 2000:
        print('The chosen amount exceeds the maximum admitted value, defaulting to 2000.')
        asset_number = 2000
    if asset_number < 1:
        print('The chosen amount is lower than the minimum admitted value, defaulting to 1.')
        asset_number = 1
    return output_name,city_name,asset_number
    
def main():
    output_name,city_name,asset_number=get_user_input()
    print(f'the type of the "output_name" variable is {type(output_name)}, and the value taken is {output_name}')
    print(f'the type of the "city_name" variable is {type(city_name)}, and the value taken is {city_name}')
    print(f'the type of the "asset_number" variable is {type(asset_number)}, and the value taken is {asset_number}')
if __name__ == '__main__':
    main()