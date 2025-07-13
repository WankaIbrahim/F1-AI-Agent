import os
from dotenv import load_dotenv
import datetime
from prompts import context
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.openai import OpenAI


def login():
    global agent, tools
    from tools import tools
    
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