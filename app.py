import os
from dotenv import load_dotenv
import boto3
import datetime
from botocore.exceptions import ClientError
from prompts import context
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import RetrieverTool

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
        raise e
    
    secret = get_secret_value_response['SecretString'].strip()      
    return secret

def load_tools():
    global tools
    from tools import tools

def login():
    global agent, tools
    os.environ["AWS_ACCESS_KEY_ID"] = "AKIAYZZGSWXPTI5RURU6"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "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"
    os.environ["OPENAI_API_KEY"] = get_secret()

    load_tools()
    
    llm = OpenAI(model="o4-mini")
    agent = ReActAgent.from_tools(
        llm=llm,
        tools=tools,
        verbose=True,
        context=context,
    )       
    return agent

def main():
    print("Welcome to the F1 Chatbot!")
    print("Type your questions and press Enter.")
    print("Type 'exit' or 'quit' to end the session.\n")

    agent = login()

    start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    history_file = f"chat_{start_time}.txt"

    def update_chat_history(text: str):
        with open(os.path.join("chat_history",history_file), "a", encoding="utf-8") as f:
            f.write(text + "\n")

        
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break

        response = agent.query(prompt)
        print(f"Agent: {response}")

        update_chat_history(f"QUERY: {prompt}")
        update_chat_history(f"ANSWER: {response}")

if __name__ == "__main__":
    load_dotenv()
    main()