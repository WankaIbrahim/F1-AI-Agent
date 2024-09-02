from llama_index.core import PromptTemplate

instruction_str = """\
    1.Convert the query to executable Python code using Pandas.
    2.The final line of code should he a Python expression that can be called with the 'eval()' function.
    3.The code should represent a solution to the query.
    4.Driver last names are ALWAYS in capital letters.
    5.Each race and sprint session has its own unique session_key.
    6.A session_key and meeting_key are NOT the same thing
    7.A record of the queries and anserwers are store in a text file and can be accessed using the "chat_history_engine" tool.
    8.To retrieve the session key for a particular session ALWAYS use the tool for that specific session
    9.PRINT ONLY THE EXPRESSION.
    10.Do not quote the expression.
"""

new_prompt = PromptTemplate(
    """\
        You are working with a pandas dataframe in Python.
        The name of the dataframe is `df`.
        This is the result of `print(df.head())`: 
        {df_str}
        
        Follow these instructions:
        {instruction_str}
        Query: {query_str}
        
        Expression:
        """
)

context = """
Purpose: The primary role of this agent is to assist users by providing accurate information about the 20 formula 1 drivers, the 10 constructors, the formula 1 meetings in 2024 and lastly every session withing those meetings.
"""