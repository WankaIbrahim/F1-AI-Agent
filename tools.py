import pandas as pd
import requests
from llama_index.core.tools import FunctionTool
from pdf_engines import create_pdf_engines
from csv_engines import create_csv_engines
import matplotlib.pyplot as plt
import numpy as np



def plot_driver_progress(session_key, driver_number):
    baseurl = "https://api.openf1.org/v1/position?session_key="
    session_key = str(session_key)
    driver_number = str(driver_number)
    position_data = requests.get(f"{baseurl}{session_key}&driver_number={driver_number}").json()
    
    position_list = []
    
    for position in position_data:
        position_information = {
            'date': pd.to_datetime(position['date']),
            'position': position['position'],
            'driver_number': position['driver_number'],
            }
        position_list.append(position_information)
    
    df = pd.DataFrame(position_list)    
    
    df.set_index('date', inplace = True)      
     
    df = df.resample('min').bfill()
   
    plt.figure(figsize=(80,40))
    
    plt.plot(
        df.index,
        df["position"],
        label = f"Driver: {driver_number}",
        color = '#1f77b4'
    )
    
    plt.xlabel("Time")
    plt.ylabel("Position")
    plt.yticks(np.arange(1, 21, step=1))
    plt.ylim(0, 21)
    plt.gca().invert_yaxis()
    plt.title("Driver Position Over Time")
    plt.legend()
    plt.grid(True)
    plt.show()    

    return plt

def get_position(session_key, driver_number):
    baseurl = "https://api.openf1.org/v1/position?session_key="
    session_key = str(session_key)
    driver_number = str(driver_number)
    position_data = requests.get(f"{baseurl}{session_key}&driver_number={driver_number}").json()
    
    position_list = []
    
    for position in position_data:
        position_information = {
            'date': pd.to_datetime(position['date']),
            'position': position['position'],
            'driver_number': position['driver_number'],
            }
        position_list.append(position_information)
    
    df = pd.DataFrame(position_list)    
    
    df.set_index('date', inplace = True)      
     
    df = df.resample('min').bfill()
    return df.iloc[-1]   

plot_engine = FunctionTool.from_defaults(
    fn=plot_driver_progress,
    name="driver_progress_plotter",
    description="this tool can create a graph of position against time for a specific driver in a specific session using a RACE session key which is an int and the drivers number which is also an int",
)

position_engine = FunctionTool.from_defaults(
    fn=get_position,
    name="driver_finishing_position",
    description="this tool can get the finishing postion for a specific driver in a specific session using the session key which is an int and the drivers number which is also an int",
)

tools = [
    plot_engine,
    position_engine,
]
tools.extend(create_csv_engines())
tools.extend(create_pdf_engines())