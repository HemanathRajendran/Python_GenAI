import os
from datetime import datetime
from zoneinfo import ZoneInfo

from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerpApiGoogleSearchTool
from dotenv import load_dotenv

load_dotenv()

today = datetime.now(ZoneInfo("Asia/Kolkata")).date().isoformat()

llm = LLM(
    model=f"azure/{os.getenv('AZURE_OPENAI_DEPLOYMENT')}",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION"),
)

# Reads SERPAPI_API_KEY from .env (serpapi.com).
search = SerpApiGoogleSearchTool()

researcher = Agent(
    role="Tech News Researcher",
    goal="Find today's top 3 distinct tech news stories from reliable sources.",
    backstory="You are a tech researcher who checks publication dates and sources.",
    tools=[search],
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

writer = Agent(
    role="Tech Newsletter Writer",
    goal="Turn the research into a clear newsletter of exactly 5 lines.",
    backstory="You are an editor who writes only from the supplied research.",
    tools=[],
    llm=llm,
    allow_delegation=False,
    verbose=True,
)

find = Task(
    description=(
        f"The system clock says today is {today}. Find the top 3 tech news stories "
        f"published today, {today}. Trust this date; do not infer the current "
        "date from your training data or claim the requested date is in the future. "
        "Call Google Search with search_query only; omit the optional location field. "
        "A timezone such as Asia/Kolkata is not a search location. "
        "If a search returns a parameter error, retry with a corrected query and no "
        "location. Do not interpret API errors as evidence about the date. "
        "Choose distinct stories by significance and check their publication dates. "
        "Use reliable sources. Do not invent facts or URLs. If you cannot verify "
        "3 stories from today, clearly report the shortfall. Do not substitute older "
        "stories or ask for date confirmation. If search fails, report the actual "
        "search error rather than guessing that the date is invalid."
    ),
    expected_output=(
        "A numbered research brief with 3 stories. For each, include the headline, "
        "publication date, source URL, a short factual summary, and why it matters. "
        "Clearly state any shortfall in verified stories."
    ),
    agent=researcher,
)

write = Task(
    description=(
        f"Write today's ({today}) 5-line tech newsletter using only the Researcher's output. "
        "Do not research or add unsupported facts. Include each story's source URL "
        "on its story line. If research is incomplete, state that in the affected "
        "story line instead of inventing a story. No blank lines or code fences."
    ),
    expected_output=(
        "Exactly 5 lines in this format:\n"
        "Tech in 5 lines\n"
        "1. <first story with source URL>\n"
        "2. <second story with source URL>\n"
        "3. <third story with source URL>\n"
        "Why it matters: <one-line explanation>"
    ),
    agent=writer,
    context=[find],
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[find, write],
    process=Process.sequential,
    verbose=True,
)

print(crew.kickoff())
