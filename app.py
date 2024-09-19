import tkinter as tk
import ttkbootstrap as ttk
from dotenv import load_dotenv
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from prompts import context
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
import os
import time
from threading import Thread


load_dotenv()

def get_secret():
    secret_name = "OPENAI_API_KEY"
    region_name = "eu-north-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if(not error_label.winfo_ismapped()):
            error_label.pack(pady=10)
        raise e
    
    error_label.destroy()
    secret = get_secret_value_response['SecretString'].strip()      
    return secret


    global agent, update_chat_history
    from tools import agent, update_chat_history

    llm = OpenAI(model="gpt-3.5-turbo")
    agent = ReActAgent.from_tools(tools=agent,
                                llm=llm,
                                verbose=True,
                                context=context)

    create_chat_window()

def login():
    global agent, update_chat_history

    # os.environ["AWS_ACCESS_KEY_ID"] = access_key_variable.get()
    # os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key_variable.get()
    
    os.environ["OPENAI_API_KEY"] = get_secret()
    
    from tools import tools, update_chat_history
    
    llm = OpenAI(model="gpt-4o")
    agent = ReActAgent.from_tools(
        llm=llm,
        tools=tools,
        verbose=True,
        context=context
    )
    login_window.destroy()
    create_chat_window()

def query():
    prompt = str(prompt_entry.get())
    result = str(agent.query(prompt))
    update_chat_history("QUERY: "+ prompt_entry.get())
    update_chat_history("ANSWER: " + result)

    result_label["text"] = result

def create_login_window():
    global login_window, access_key_variable, secret_key_variable, error_label

    login_window = ttk.Window(themename='flatly')
    login_window.title('F1 Chatbot')
    login_window.geometry('2880x1800')

    title_label = ttk.Label(master=login_window, text="Welcome to F1 Chatbot", font='Times 24')
    title_label.pack(pady=20)

    error_label = ttk.Label(master=login_window, text='Invalid Credentials', font='Times 18', foreground='red')


    access_key_frame = ttk.Frame(master=login_window)
    access_key_variable = ttk.StringVar()
    access_key_label = ttk.Label(master=access_key_frame, text="AWS ACCESS KEY ID", font='Calibri 12')
    access_key_label.pack(side = 'left', padx=5)
    access_key_entry = ttk.Entry(master=access_key_frame, textvariable=access_key_variable, width=50)
    access_key_entry.pack(side = 'left', padx=5)
    access_key_frame.pack(pady=5)

    secret_key_frame = ttk.Frame(master=login_window)
    secret_key_variable = ttk.StringVar()
    secret_key_label = ttk.Label(master=secret_key_frame, text="AWS SECRET ACCESS KEY ID", font='Calibri 12')
    secret_key_label.pack(side = 'left', padx=5)
    secret_key_entry = ttk.Entry(master=secret_key_frame, textvariable=secret_key_variable, width=50)
    secret_key_entry.pack(side = 'left', padx=5)
    secret_key_frame.pack(pady=5)


    login_button = ttk.Button(master=login_window, text='Login', command=login)
    login_button.pack(pady=20)

    login_window.mainloop()

def create_chat_window():
    global prompt_entry, result_label

    chat_window = ttk.Window(themename="flatly")
    chat_window.title('F1 Chatbot')
    chat_window.geometry('2880x1800')


    title_label = ttk.Label(master = chat_window, text = "F1 Chatbot", font = 'Times 36', background='#ffffff')
    title_label.pack(pady=100)

    prompt_frame = ttk.Frame(master=chat_window)
    prompt_entry = ttk.Entry(master=prompt_frame, width=100)
    submit_button = ttk.Button(master=prompt_frame, text="Submit", command=query)

    prompt_entry.pack(side = 'left', padx = 10)
    submit_button.pack(side = 'left', padx=10)
    prompt_frame.pack(pady=10)

    result_label = ttk.Label(master=chat_window, font='Calibri 16', background='#ffffff')    
    result_label.pack(pady=50)

if __name__ == "__main__":
    create_login_window()
