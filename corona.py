"""
This program can run various test against the Covid19 data tracking API endpoint
For help, run:
corona.py --help

Author: Niko Kirilenko

"""

import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c','--country',action='store',dest='country',help='Select a country')
user_input = parser.parse_args()

print (user_input.country)

# API call against the endpoint
# Endpoint details can be found at : https://rapidapi.com/slotixsro-slotixsro-default/api/covid-19-tracking/endpoints
URL = "https://covid-19-tracking.p.rapidapi.com/v1"
HEADERS = {
        'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com",
        'x-rapidapi-key': "7991b48f62mshf6b2d8b813a28a4p1f3592jsn0a7b0b65fe6e"
    }
response = requests.request("GET", URL, headers=HEADERS).json()


# Get a list of all of the countries upon you may run the queries
available_country_list = []
for i in range(len(response)-1):  # The last index of the variable contains only information on the last update time
    available_country_list.append(response[i]['Country_text'].lower())


try:
    print('Country name: ' + user_input.country.capitalize())
    print('Active cases: ' + response[available_country_list.index(user_input.country.lower())]['Active Cases_text'])
    print('New cases: ' + response[available_country_list.index(user_input.country.lower())]['New Cases_text'])
    print('New deaths: ' + response[available_country_list.index(user_input.country.lower())]['New Deaths_text'])
    print('Total cases: ' + response[available_country_list.index(user_input.country.lower())]['Total Cases_text'])
    print('Total deaths: ' + response[available_country_list.index(user_input.country.lower())]['Total Deaths_text'])
    print('Total recoverd: ' + response[available_country_list.index(user_input.country.lower())]['Total Recovered_text'])
except ValueError:
    print("The country you provided is not in the list.")




