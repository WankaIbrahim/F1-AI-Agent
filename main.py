import os
import pandas as pd
from dotenv import load_dotenv
from prompts import context
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from tools import tools, update_chat_history

                                           
load_dotenv()
            
llm = OpenAI(model="gpt-4o")

agent = ReActAgent.from_tools(tools=tools,
                              llm=llm,
                              verbose=True,
                              context=context)

while (prompt := input("Enter a prompt (q to quit):  ")) != "q":
    try:
        result = agent.query(prompt)
        update_chat_history("QUERY: "+ prompt)
        update_chat_history("ANSWER: " + str(result))
        print(result)
    except Exception as e:
        print(f"Error: {e}")
