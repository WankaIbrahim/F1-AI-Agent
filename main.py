import os
import pandas as pd
from dotenv import load_dotenv
from prompts import context
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from csv_generator import generate_csv_files, baseurl
generate_csv_files(baseurl)
from tools import tools
from google.cloud import secretmanager

load_dotenv()

#TODO Figure out how to include the OpenAI_api_key using google secrets manager
# def get_api_key(project_id, secret_id, version_id="latest") -> str:
#     name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
#     response = client.access_secret_version(name=name)
#     return response.payload.data.decode('UTF-8')
    
                                            
             
            
llm = OpenAI(model="gpt-4o")
agent = ReActAgent.from_tools(tools=tools,
                              llm=llm,
                              verbose=True,
                              context=context)

while (prompt := input("Enter a prompt (q to quit):  ")) != "q":
    try:
        result = agent.query(prompt)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
