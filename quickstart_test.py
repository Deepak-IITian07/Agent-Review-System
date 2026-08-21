from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
load_dotenv()


llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

researcher = Agent(
    role="Researcher",
    goal="Find 3 interesting facts about a given topic",
    backstory="You are a curious researcher who loves discovering facts.",
    llm=llm,
    verbose=True
)

task = Task(
    description="Find 3 interesting facts about Jaipur city in India.",
    expected_output="A bullet list of 3 facts",
    agent=researcher
)

crew = Crew(agents=[researcher], tasks=[task])
result = crew.kickoff()
print(result)