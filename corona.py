"""
This program can run various test against the Covid19 data tracking API endpoint
For help, run:
corona.py --help

Author: Niko Kirilenko

"""

import requests
import argparse
import sys
import os

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-c','--country',action='store',dest='country_parse',help='Select a country')
group.add_argument('-f','--filter',action='store',dest='filter_parse',help='Search globally and filter the results. \n'
                        'Available filters are:\n'
                        'active_cases < > = \n '
                        'new_cases < > = \n'
                        'new_deaths < > =\n'
                        'total_cases < > = \n'
                        'total_recovered < > = \n'
                        'total_deaths < > =')

user_input = parser.parse_args()
database = {}

URL = "https://covid-19-tracking.p.rapidapi.com/v1"
HEADERS = {
        'x-rapidapi-host': "covid-19-tracking.p.rapidapi.com",
        'x-rapidapi-key': "7991b48f62mshf6b2d8b813a28a4p1f3592jsn0a7b0b65fe6e"
    }
response = requests.request("GET", URL, headers=HEADERS).json()


class Country:
    def __init__(self, name, active_cases, new_cases, new_deaths, total_cases, total_recovered,total_deaths):
        self.name = name
        self.active_cases = active_cases
        self.new_cases = new_cases
        self.new_deaths = new_deaths
        self.total_cases = total_cases
        self.total_recovered = total_recovered
        self.total_deaths = total_deaths

    def show_statistics(self):
        print("Name: " + self.name + "\n"
               + "Active cases: " + self.active_cases + "\n"
               + "New cases: " + self.new_cases + "\n"
               + "New deaths: " + self.new_deaths + "\n"
               + "Total deaths: " + self.total_deaths + "\n"
               + "Total cases: " + self.total_cases + "\n"
               + "Total recovered: " + self.total_recovered)


for i in range(len(response)-1):
    database[response[i]['Country_text']] = (Country(name=response[i]['Country_text'].replace(',', ''),
                             active_cases=response[i]['Active Cases_text'].replace(',', ''),
                             new_cases=response[i]['New Cases_text'].replace(',', '').replace('+', ''),
                             new_deaths=response[i]['New Deaths_text'].replace(',','').replace('+', ''),
                             total_cases=response[i]['Total Cases_text'].replace(',', ''),
                             total_deaths=response[i]['Total Deaths_text'].replace(',', ''),
                             total_recovered=response[i]['Total Recovered_text'].replace(',', '')))


def os_check_and_countries_output(file,path):
    file = open(file, "w")
    for key in database:
        file.write(key + "\n")
    file.close()
    print("Done. Please check file: " + os.getcwd() + path)




if user_input.filter_parse is None:
    if user_input.country_parse.capitalize() in database:
        database[user_input.country_parse.capitalize()].show_statistics()
    else:
        print("Unknown country name.")
        print("Generating file with the available countries you can run the command against... ")
        if sys.platform == 'win32':
            os_check_and_countries_output("CountriesList.txt", "\CountriesList.txt")
        else:
            os_check_and_countries_output("CountriesList", "/CountriesList.txt")

else:
    filter_input = user_input.filter_parse.split()
    if filter_input[1] == '=':
        for key in database:
            if getattr(database[key],filter_input[0]) == filter_input[2]:
                database[key].show_statistics()
                print("\n")

    elif filter_input[1] == '>':
        for key in database:
            try:
                if int(getattr(database[key], filter_input[0])) > int(filter_input[2]):
                    database[key].show_statistics()
                    print("\n")
            except ValueError:
                continue


    elif filter_input[1] == '<':
        for key in database:
            try:
                if int(getattr(database[key], filter_input[0])) < int(filter_input[2]):
                    database[key].show_statistics()
                    print("\n")
            except ValueError:
                continue







