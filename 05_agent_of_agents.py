import os

from crewai import Crew, Process
from dotenv import load_dotenv

from society_of_minds.mind_creator import TheMind

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# What task do you want to give to the mind
task = "Create powerpoint explain the impact of technology on climate."
print("Mind has got the task to perform: {task}".format(task = task))

# Instantiate the mind
the_mind = TheMind()
# Mind now creates the tiny agents which are mindless
crew_agents, crew_tasks = the_mind.create_the_society(task)

print("Society of mind now working on the task...")
crew = Crew(
    agents=crew_agents,
    tasks=crew_tasks,
    verbose=False,
    process=Process.sequential  # Optional: Sequential task execution is default
)

# Society of minds at work
result = crew.kickoff()
print(result)
