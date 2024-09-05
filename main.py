import os
import pandas as pd
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from prompts import context
from llama_index.core.agent import ReActAgent
import openai

load_dotenv()

def get_secret():


    secret_name = "OPENAI_API_KEY"
    region_name = "eu-north-1"

    # Create a Secrets Manager client
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
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    secret = get_secret_value_response['SecretString'].strip()      
    return secret
OPENAI_API_KEY = get_secret()
print(OPENAI_API_KEY)

from tools import tools, update_chat_history


llm = openai(model="gpt-4o",
             api_key=OPENAI_API_KEY)

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
