import os
import pandas as pd
from prompts import INSTRUCTIONS_BY_NAME, PROMPTS_BY_NAME
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from csv_generator import generate_csv_files, baseurl


generate_csv_files(baseurl)

def create_csv_engines():
    folder_path = os.path.join("data", "csv_files")
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    tools = []

    for file in csv_files:
        name = file.replace(".csv", "")
        df = pd.read_csv(os.path.join(folder_path, file))

        engine = PandasQueryEngine(
            df=df,
            verbose=True,
            instruction_str=INSTRUCTIONS_BY_NAME[name],
        )
        engine.update_prompts({"pandas_prompt": PROMPTS_BY_NAME[name]})

        tools.append(
            QueryEngineTool(
                query_engine=engine,
                metadata=ToolMetadata(
                    name=name,
                    description=f"{name} data for 2024 F1 season",
                ),
            )
        )
    return tools
