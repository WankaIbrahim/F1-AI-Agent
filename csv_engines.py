from dotenv import load_dotenv
import os
import pandas as pd
from prompts import new_prompt, instruction_str, context
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from csv_generator import generate_csv_files, baseurl
generate_csv_files(baseurl)

load_dotenv()


def create_csv_engines():
    folder_path = os.path.join("data", "csv_files")
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    query_engine_tools = []

    for csv_file in csv_files:
        csv_path = os.path.join(folder_path, csv_file)
        csv_df = pd.read_csv(csv_path)
        name = csv_file.replace(".csv", "")
        description = f"This tool provides information about all the {csv_file.replace(".csv", "")}."


        csv_query_engine = PandasQueryEngine(
            df=csv_df,
            verbose=True,
            instruction_str=instruction_str
        )

        csv_query_engine.update_prompts({"pandas_prompt": new_prompt})

        query_engine_tools.append(
            QueryEngineTool(
            query_engine = csv_query_engine,
            metadata=ToolMetadata(
                name=name,
                description=description
            )
            )
        ) 
    return query_engine_tools

