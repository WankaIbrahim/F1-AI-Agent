import requests
import os
import pandas as pd

baseurl = "https://api.openf1.org/v1/"


#All data is taken from the 2024 Formula 1 season

def get_drivers(baseurl):
    drivers_data = requests.get(baseurl + f'drivers?meeting_key>=1229&session_key=9574').json()
    
    driver_list = []
    for driver in drivers_data:
        driver_information = {
            'first_name': driver['first_name'],
            'last_name': driver['last_name'],
            'driver_number': driver['driver_number'],
            'country_code': driver['country_code'],
            'team_name': driver['team_name'],
        }
        driver_list.append(driver_information)
    
    driver_dataframe = pd.DataFrame(driver_list)
    driver_dataframe.to_csv(os.path.join('data', 'csv_files', 'drivers.csv'), index=False)
    
def get_race_sessions(baseurl):
    session_data = requests.get(baseurl + f'sessions?year=2024&session_name=Race').json()
    
    session_list = []
    for session in session_data:
        session_information = {        
            'session_key': session['session_key'],
            'circuit_short_name': session['circuit_short_name'],
            'country_name': session['country_name'],
            'location': session['location'],
        }
        session_list.append(session_information)
    
    session_dataframe = pd.DataFrame(session_list)
    session_dataframe.to_csv(os.path.join('data', 'csv_files', 'race_sessions.csv'), index=False)
    
def get_sprint_sessions(baseurl):
    session_data = requests.get(baseurl + f'sessions?year=2024&session_name=Sprint').json()
    
    session_list = []
    for session in session_data:
        session_information = {       
            'session_key': session['session_key'],
            'circuit_short_name': session['circuit_short_name'],
            'country_name': session['country_name'],
            'location': session['location'],
        }
        session_list.append(session_information)
    
    session_dataframe = pd.DataFrame(session_list)
    session_dataframe.to_csv(os.path.join('data', 'csv_files', 'sprint_sessions.csv'), index=False)
    

    
def generate_csv_files(baseurl):
    get_drivers(baseurl)
    get_race_sessions(baseurl)
    get_sprint_sessions(baseurl)



