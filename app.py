import os
from dotenv import load_dotenv
import datetime
from prompts import context
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.openai import OpenAI
from PySide6.QtCore import QObject, Slot, Signal
import asyncio
import nest_asyncio
nest_asyncio.apply()

async def get_response(agent, prompt):
    response = await agent.run(prompt)
    print("Agent final response:", response)
    return response

class ChatBotBackend(QObject):
    responseReady = Signal(str)

    def __init__(self):
        super().__init__()
        self.agent = None
        self.history_file = None
        self.init_agent()

    def init_agent(self):
        load_dotenv()
        global agent, tools
        from tools import tools


        llm = OpenAI(model="o4-mini")
        self.agent = ReActAgent(
            llm=llm,
            tools=tools,
            verbose=True,
            context=context,
        )

        start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        if not os.path.exists("chat_history"):
            os.makedirs("chat_history")
        self.history_file = os.path.join("chat_history", f"chat_{start_time}.txt")

    def update_chat_history(self, text: str):
        with open(self.history_file, "a", encoding="utf-8") as f:
            f.write(text + "\n")

    @Slot(str)
    def sendQuery(self, prompt: str):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if not prompt.strip():
            self.responseReady.emit("Please enter a question.")
            return

        response = loop.run_until_complete(get_response(self.agent, prompt))

        self.update_chat_history(f"QUERY: {prompt}")
        self.update_chat_history(f"ANSWER: {response}")

        self.responseReady.emit(str(response))