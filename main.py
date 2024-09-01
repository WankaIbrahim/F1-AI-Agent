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

                                           
load_dotenv()
            
llm = OpenAI(model="gpt-4o")
OpenAI.api_key = os.getenv("OPENAI_API_KEY")
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
