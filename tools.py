from dotenv import load_dotenv
import os
import pandas as pd
from prompts import new_prompt, instruction_str, context
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from plot import plot_engine
from csv_generator import baseurl
import requests
from llama_index.core.tools import FunctionTool
from pdf import engines

load_dotenv()

drivers_path = os.path.join("data", "drivers.csv")
drivers_df = pd.read_csv(drivers_path)

meetings_path = os.path.join("data", "meetings.csv")
meetings_df = pd.read_csv(meetings_path)

practice_sessions_path = os.path.join("data", "practice_sessions.csv")
practice_sessions_df = pd.read_csv(practice_sessions_path)

qualifying_sessions_path = os.path.join("data", "qualifying_sessions.csv")
qualifying_sessions_df = pd.read_csv(qualifying_sessions_path)

race_sessions_path = os.path.join("data", "race_sessions.csv")
race_sessions_df = pd.read_csv(race_sessions_path)

sprint_sessions_path = os.path.join("data", "sprint_sessions.csv")
sprint_sessions_df = pd.read_csv(sprint_sessions_path)


drivers_qe = PandasQueryEngine(
    df=drivers_df,
    verbose=True,
    instruction_str=instruction_str
)
drivers_qe.update_prompts({"pandas_prompt": new_prompt})

meetings_qe = PandasQueryEngine(
    df=meetings_df,
    verbose=True,
    instruction_str=instruction_str
)
meetings_qe.update_prompts({"pandas_prompt": new_prompt})

practice_sessions_qe = PandasQueryEngine(
    df=practice_sessions_df,
    verbose=True,
    instruction_str=instruction_str
)
practice_sessions_qe.update_prompts({"pandas_prompt": new_prompt})

qualifying_sessions_qe = PandasQueryEngine(
    df=qualifying_sessions_df,
    verbose=True,
    instruction_str=instruction_str
)
qualifying_sessions_qe.update_prompts({"pandas_prompt": new_prompt})

race_sessions_qe = PandasQueryEngine(
    df=race_sessions_df,
    verbose=True,
    instruction_str=instruction_str
)
race_sessions_qe.update_prompts({"pandas_prompt": new_prompt})

sprint_sessions_qe = PandasQueryEngine(
    df=sprint_sessions_df,
    verbose=True,
    instruction_str=instruction_str
)
sprint_sessions_qe.update_prompts({"pandas_prompt": new_prompt})

###############################################################

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
    
    

position_engine = FunctionTool.from_defaults(
    fn=get_position,
    name="driver_finishing_position",
    description="this tool can get the finishing postion for a specific driver in a specific session using the session key which is an int and the drivers number which is also an int",
)


###############################################################

tools = [
    QueryEngineTool(query_engine=drivers_qe,
                    metadata=ToolMetadata(
                        name="drivers_data",
                        description="This gives information about the 20 formula 1 drivers"
                    ),
    ),
    QueryEngineTool(query_engine=meetings_qe,
                    metadata=ToolMetadata(
                        name="meetings_data",
                        description="This gives information about the 2024 Formula 1 meetings that have taken place."
                    ),
    ),
    QueryEngineTool(query_engine=practice_sessions_qe,
                    metadata=ToolMetadata(
                        name="practice_sessions_data",
                        description="This gives information about all the practice sessions that have taken place"
                    ),
    ),
    QueryEngineTool(query_engine=qualifying_sessions_qe,
                    metadata=ToolMetadata(
                        name="qualifying_sessions_data",
                        description="This gives information about all the qualifying sessions that have taken place"
                    ),
    ),
    QueryEngineTool(query_engine=race_sessions_qe,
                    metadata=ToolMetadata(
                        name="race_sessions_data",
                        description="This gives information about all the race sessions that have taken place"
                    ),
    ),
    QueryEngineTool(query_engine=sprint_sessions_qe,
                    metadata=ToolMetadata(
                        name="sprint_sessions_data",
                        description="This gives information about all the sprint sessions that have taken place"
                    ),
    ),
    plot_engine,
    position_engine,
    
]

tools.extend(engines)