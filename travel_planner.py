from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv
import os

load_dotenv()

city = input("Which city? ")

llm = LLM(
    model=f"azure/{os.getenv('AZURE_OPENAI_DEPLOYMENT')}",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION")
)

planner = Agent(
    role="Travel Planner",
    goal="Recommend the best tourist attractions in a city for first-time visitors.",
    backstory=(
        "You are an experienced travel planner who helps travelers discover "
        "popular attractions, cultural landmarks, and must-visit locations. "
        "You provide concise and practical recommendations."
    ),
    verbose=True,
    llm=llm
)

task = Task(
    description=(
        "Suggest exactly 3 places to visit in {city}. "
        "For each place, provide a one-line description and why it is worth visiting."
    ),
    expected_output=(
        "A numbered list containing exactly 3 places. "
        "Each item should include the place name and a short explanation."
    ),
    agent=planner
)

crew = Crew(
    agents=[planner],
    tasks=[task],
    verbose=True
)

result = crew.kickoff(inputs={"city": city})

print("\nTravel Recommendations:\n")
print(result)
