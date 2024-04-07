import os

from crewai import Crew, Agent, Task, Process
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

father_agent = Agent(
    role='Father',
    goal='You are the father of a kid. The kid may ask you any question.'
         'Your goal is to provide a satisfactory answer to the kid.',
    verbose=True,
    memory=True,
    backstory=(
        "You are a 40 year old male. You live in the city of San Jose with your wife and kid who is 10 years old."
    ),
    tools=[],
    allow_delegation=True
)

father_task = Task(
    description=(
        "Your task is to answer the {question} of your kid in a satisfactory "
        "and legible way so that it makes sense to your kid. "
    ),
    expected_output='Answer to your kid question',
    tools=[],
    # human_input = True,
    agent=father_agent
)

parent_crew = Crew(
    agents=[father_agent],
    tasks=[father_task],
    process=Process.sequential,
    memory=True,
    verbose=True,
    embedder={
        "provider": "openai",
        "config": {
            "model": 'text-embedding-3-small'
        }
    }
)

while True:
    question = input("Kid: \n")
    answer = parent_crew.kickoff({"question": question})

    print("***********************")
    print(answer)
