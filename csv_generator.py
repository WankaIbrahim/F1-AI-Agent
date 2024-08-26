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
            'full_name': driver['full_name'],
            'name_acronym': driver['name_acronym'],
            'driver_number': driver['driver_number'],
            'country_code': driver['country_code'],
            'team_name': driver['team_name'],
            'goat_status': 0
        }
        if(driver_information['first_name']=='Lewis'):
            driver_information['goat_status'] = 1
        driver_list.append(driver_information)
    
    driver_dataframe = pd.DataFrame(driver_list)
    driver_dataframe.to_csv(os.path.join('data','drivers.csv'), index=False)
    
def get_race_sessions(baseurl):
    session_data = requests.get(baseurl + f'sessions?year=2024&session_name=Race').json()
    
    session_list = []
    for session in session_data:
        session_information = {
            'meeting_key': session['meeting_key'],        
            'session_key': session['session_key'],
            'circuit_key': session['circuit_key'],
            'circuit_short_name': session['circuit_short_name'],
            'country_key': session['country_key'],
            'country_name': session['country_name'],
            'location': session['location'],
            'gmt_offset': session['gmt_offset'],
            'start_date': session['date_start'],
            'end_date': session['date_end'],
        }
        session_list.append(session_information)
    
    session_dataframe = pd.DataFrame(session_list)
    session_dataframe.to_csv(os.path.join('data', 'race_sessions.csv'), index=False)
    
def get_sprint_sessions(baseurl):
    session_data = requests.get(baseurl + f'sessions?year=2024&session_name=Sprint').json()
    
    session_list = []
    for session in session_data:
        session_information = {
            'meeting_key': session['meeting_key'],        
            'session_key': session['session_key'],
            'circuit_key': session['circuit_key'],
            'circuit_short_name': session['circuit_short_name'],
            'country_key': session['country_key'],
            'country_name': session['country_name'],
            'location': session['location'],
            'gmt_offset': session['gmt_offset'],
            'start_date': session['date_start'],
            'end_date': session['date_end'],
        }
        session_list.append(session_information)
    
    session_dataframe = pd.DataFrame(session_list)
    session_dataframe.to_csv(os.path.join('data', 'sprint_sessions.csv'), index=False)
    
def get_qualifying_sessions(baseurl):
    session_data = requests.get(baseurl + f'sessions?year=2024&session_name=Qualifying').json()
    
    session_list = []
    for session in session_data:
        session_information = {
            'meeting_key': session['meeting_key'],        
            'session_key': session['session_key'],
            'circuit_key': session['circuit_key'],
            'circuit_short_name': session['circuit_short_name'],
            'country_key': session['country_key'],
            'country_name': session['country_name'],
            'location': session['location'],
            'gmt_offset': session['gmt_offset'],
            'start_date': session['date_start'],
            'end_date': session['date_end'],
        }
        session_list.append(session_information)
    
    session_dataframe = pd.DataFrame(session_list)
    session_dataframe.to_csv(os.path.join('data', 'qualifying_sessions.csv'), index=False)
    
def get_practice_sessions(baseurl):
    session_data = requests.get(baseurl + f'sessions?year=2024&session_type=Practice').json()
    
    session_list = []
    for session in session_data:
        session_information = {
            'meeting_key': session['meeting_key'],        
            'session_key': session['session_key'],
            'circuit_key': session['circuit_key'],
            'circuit_short_name': session['circuit_short_name'],
            'country_key': session['country_key'],
            'country_name': session['country_name'],
            'location': session['location'],
            'gmt_offset': session['gmt_offset'],
            'start_date': session['date_start'],
            'end_date': session['date_end'],
        }
        session_list.append(session_information)
    
    session_dataframe = pd.DataFrame(session_list)
    session_dataframe.to_csv(os.path.join('data', 'practice_sessions.csv'), index=False)
    
def get_meetings(baseurl):
    meeting_data = requests.get(baseurl + f'meetings?year=2024').json()
    
    meeting_list = []
    for meeting in meeting_data:
        meeting_information = {
            'meeting_key': meeting['meeting_key'],
            'meeting_official_name': meeting['meeting_official_name'],     
            'circuit_key': meeting['circuit_key'],
            'circuit_short_name': meeting['circuit_short_name'],
            'country_key': meeting['country_key'],
            'country_name': meeting['country_name'],
            'location': meeting['location'],
            'gmt_offset': meeting['gmt_offset'],
            'start_date': meeting['date_start'],
        }
        meeting_list.append(meeting_information)
    
    meeting_dataframe = pd.DataFrame(meeting_list)
    meeting_dataframe.to_csv(os.path.join('data', 'meetings.csv'), index=False)

    
def generate_csv_files(baseurl):
    get_drivers(baseurl)
    get_race_sessions(baseurl)
    get_sprint_sessions(baseurl)
    get_qualifying_sessions(baseurl)
    get_practice_sessions(baseurl)
    get_meetings(baseurl)



