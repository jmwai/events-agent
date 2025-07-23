import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.tools import google_search, tool

@tool
def get_city(city: str) -> str:
    """Returns the city name from the location string"""
    available_cities = ["nairobi", "mombasa"]
    if city.lower() in available_cities:
        return city
    else:
        raise ValueError(f"Sorry, I don't have events for {city}.")

@tool
def get_start_date() -> str:
    """Returns the current date in Africa/Nairobi timezone"""
    tz = ZoneInfo("Africa/Nairobi")
    now = datetime.datetime.now(tz)
    return now.strftime("%Y-%m-%d")

@tool
def get_end_date() -> str:
    """Returns the date two days from now in Africa/Nairobi timezone"""
    tz = ZoneInfo("Africa/Nairobi")
    now = datetime.datetime.now(tz)
    return (now + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

root_agent = Agent(
    name="Executor",
    model="gemini-2.0-pro-vision",  # or gemini-2.0-pro if you want function calling support
    description="Finds events and attractions in a city",
    instruction="""
        You're an AI executor. Use tools like google_search, get_city, get_start_date, and get_end_date
        to find and return events in a given city between given dates. 
        Return the plan as a JSON list of events under the 'plan' key.
    """,
    tools=[google_search, get_city, get_start_date, get_end_date],
    output_key="plan"
)

#message="Find me a weekend plan for Nairobi between 2025-07-25 and 2025-07-27",