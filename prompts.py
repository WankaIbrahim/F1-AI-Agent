from llama_index.core import PromptTemplate

instruction_str = """\
    1.Convert the query to executable Python code using Pandas.
    2.The final line of code should he a Python expression that can be called with the 'eval()' function.
    3.The code should represent a solution to the query.
    4.Driver last names are ALWAYS in capital letters
    5.A meeting consists of all the sessions held at a particular track which includes all practice_sessions, qualifying_sessions, race_sessions and sprint_sessions.
    6.Each meeting has a meeting_key which all sessions that took place during that meeting share.
    7.Each session has a unique session_key which no other session has.
    8.PRINT ONLY THE EXPRESSION.
    9.Do not quote the expression.
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
Purpose: The primary role of this agent is to assist users by providing accurate information about the 20 formula 1 drivers, the formula 1 meetings in 2024 and lastly every session withing those meetings.
The data is sourced from the OpenF1 api.
"""