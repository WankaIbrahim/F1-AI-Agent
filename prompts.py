from llama_index.core import PromptTemplate

#CONTEXT
context = """
You are a Formula 1 data assistant. Your tools let you:

- Query CSVs:
  - drivers            -> columns: first_name, last_name, driver_number, country_code, team_name
  - race_sessions      -> columns: session_key, circuit_short_name, country_name, location
  - sprint_sessions    -> same schema as race_sessions (sprint events only)

- Call function tools:
  - driver_finishing_position(session_key: int, driver_number: int)
      -> returns the finishing-position row for that driver/session
  - driver_progress_plotter(session_key: int, driver_number: int)
      -> returns a matplotlib figure of position-vs-time

Rules:
1. Always fetch the numeric session_key first (from race_sessions or sprint_sessions) before
   calling driver_* tools.
2. Always fetch the driver_number from the drivers CSV before calling driver_* tools.
3. "Great Britain" is the canonical value in country_name for the British Grand Prix
   (users may say "United Kingdom", "Britain", "British GP", "Silverstone GP").
4. Provide concise, factual answers. Include units (e.g., "P1", "4 points", "lap 12") when relevant.
"""

# BASE INSTRUCTIONS FOR ANY PANDAS ENGINE
BASE_PANDAS_RULES = """
1. Convert the user query into valid pandas code that uses the DataFrame `df`.
2. The final line of your code must be a single expression suitable for eval().
3. Do not call print(), do not wrap in quotes, do not add prose or code fences.
4. Output only that final expression - nothing else.
"""

# DRIVERS CSV PROMPT
drivers_instruction_str = BASE_PANDAS_RULES + """
5. Column reference guide:
   first_name, last_name (Capitalized), driver_number, country_code, team_name
6. If the question is "What number is <driver>?" or similar, return
   df[df['last_name'].str.lower() == '<surname_in_lower>']['driver_number'].iloc[0]
7. Last names in the CSV are capitalized (e.g., 'Norris', 'Verstappen'); match case-insensitively using `.str.lower()`. Always convert the literal in the code to lowercase as well.
8. Do NOT return unrelated columns when the user asks for the number.
"""

drivers_prompt = PromptTemplate(
    """
You are working with the Drivers DataFrame (`df`).

Preview (`df.head()`):
{df_str}

Follow the instructions exactly:

{instruction_str}

Query: {query_str}

Expression:
""")

# RACE‑SESSION CSV PROMPT
race_instruction_str = BASE_PANDAS_RULES + """
5. Column reference guide:
   session_key (int), circuit_short_name, country_name, location
6. If the query is "What is the session key for <race> ...":
   - First try to match country_name exactly.
   - If the race is British GP (user may say "United Kingdom", "UK", "Silverstone", etc.),
     treat it as 'Great Britain'.
7. Return the session_key, never the circuit name.
8. Example expression for British GP:
   df.loc[df['country_name'] == 'Great Britain', 'session_key'].iloc[0]
"""

race_prompt = PromptTemplate(
    """
You are working with the Race Sessions DataFrame (`df`).

Preview (`df.head()`):
{df_str}

Follow the instructions exactly:

{instruction_str}

Query: {query_str}

Expression:
""")


# SPRINT‑SESSION CSV PROMPT
sprint_instruction_str = race_instruction_str.replace(
    "Race Sessions", "Sprint Sessions"
).replace(
    "Race GP", "Sprint"
)

sprint_prompt = PromptTemplate(
    """
You are working with the Sprint Sessions DataFrame (`df`).

Preview (`df.head()`):
{df_str}

Follow the instructions exactly:

{instruction_str}

Query: {query_str}

Expression:
""")


PROMPTS_BY_NAME = {
    "drivers": drivers_prompt,
    "race_sessions": race_prompt,
    "sprint_sessions": sprint_prompt,
}

INSTRUCTIONS_BY_NAME = {
    "drivers": drivers_instruction_str,
    "race_sessions": race_instruction_str,
    "sprint_sessions": sprint_instruction_str,
}