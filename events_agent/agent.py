import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import FunctionTool, google_search

GEMINI_MODEL = "gemini-2.5-flash"


# === Internal tools for city and date info ===
def get_city() -> str:
    """Returns a city name. You can customize this to use user input."""
    return "Nairobi"

def get_start_date() -> str:
    """Today's date in Africa/Nairobi timezone."""
    now = datetime.datetime.now(ZoneInfo("Africa/Nairobi"))
    return now.strftime("%Y-%m-%d")

def get_end_date() -> str:
    """Two days from now in Africa/Nairobi timezone."""
    now = datetime.datetime.now(ZoneInfo("Africa/Nairobi"))
    return (now + datetime.timedelta(days=30)).strftime("%Y-%m-%d")


# === info_agent ===

info_agent = Agent(
    name="info_agent",
    model=GEMINI_MODEL,
    description="Gathers city and date info.",
    instruction="""
        Use get_city, get_start_date, and get_end_date tools.
        Store results in session_state["city"], ["start_date"], and ["end_date"].
    """,
    tools=[get_city, get_start_date, get_end_date]
)

# === search_agent ===

search_agent = Agent(
    name="search_agent",
    model=GEMINI_MODEL,
    description="Finds events using google_search.",
    instruction="""
        Use google_search to find top 10 events in session_state["city"] 
        between session_state["start_date"] and session_state["end_date"].
        Return the results in a JSON format.
    """,
    tools=[google_search]
)

# === root_agent ===

root_agent = SequentialAgent(
    name="event_planner_root",
    description="Plans events by combining info_agent and search_agent.",
    sub_agents=[info_agent, search_agent],
)

