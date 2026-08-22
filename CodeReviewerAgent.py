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


# single agent Crew(..) line
# crew = Crew(agents=[reviewer], tasks=[review_task])
# result = crew.kickoff()
# print(result)

# test writer crew agent created
test_writer = Agent(
    role="Test Engineer",
    goal="Write pytest tests covering edge cases and bugs found",
    backstory="You are a QA engineer who writes thorough, runnable pytest test suites.",
    llm=llm,
    verbose=True
)

# bug fixer crew agent created
fixer = Agent(
    role="Bug Fixer",
    goal="Rewrite the code fixing all identified issues",
    backstory="You are a senior engineer who writes clean, corrected code based on review feedback.",
    llm=llm,
    verbose=True
)

test_task = Task(
    description="Write pytest tests for the issues found in this review:\n{review}",
    expected_output="Complete, runnable pytest test file content",
    agent=test_writer,
    context=[review_task]
)

fix_task = Task(
    description="Fix the code based on this review:\n{review}",
    expected_output="Complete corrected Python code",
    agent=fixer,
    context=[review_task]
)

crew = Crew(agents=[reviewer, test_writer, fixer], tasks=[review_task, test_task, fix_task] , process="sequential")

result = crew.kickoff()
print(result)