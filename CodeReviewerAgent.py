from crewai import Agent, Task, Crew, LLM
import os
from dotenv import load_dotenv
load_dotenv()

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

reviewer = Agent(
    role="Senior Code Reviewer",
    goal="Find bugs, bad practices, and missing edge cases in Python code",
    backstory="You are a meticulous senior engineer who reviews PRs for a living.",
    llm=llm,
    verbose=True
)

with open("sample_code.py") as f:
    code = f.read()

review_task = Task(
    description=f"Review this Python code and list issues:\n\n{code}",
    expected_output="A bullet list of issues found, with severity (low/medium/high)",
    agent=reviewer
)

crew = Crew(agents=[reviewer], tasks=[review_task])
result = crew.kickoff()
print(result)