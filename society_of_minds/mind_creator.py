import ast
import os
from typing import List

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


class Agents(BaseModel):
    agent_name: str
    role: str
    goal: str
    backstory: str
    task: str
    taskoutput: str


class AgentList(BaseModel):
    agents: List[Agents]

    class Config:
        arbitrary_types_allowed = True


class TheMind(BaseModel):

    def create_agent_tasks(self, agent_info):
        crew_agents = []
        crew_tasks = []
        for agent in agent_info:
            agent_name = agent["agent_name"]
            print(f"Creating agent {agent_name}".format(agent_name=agent_name))
            role_name = agent["role"]
            goal = agent["goal"]
            backstory = agent["backstory"]
            task = agent["task"]
            task_output = agent["taskoutput"]
            crew_agent = Agent(
                role=role_name,
                goal=goal,
                verbose=False,
                memory=True,
                backstory=backstory,
                tools=[],
                allow_delegation=False
            )
            crew_agents.append(crew_agent)
            print("Creating task for the agent {task} :".format(task=task))
            crew_task = Task(
                description=(
                    task
                ),
                expected_output=task_output,
                tools=[],
                agent=crew_agent
            )
            crew_tasks.append(crew_task)
        # for agent in crew_agents:
        #     print(agent.role)
        print("---------------------------------")
        return crew_agents, crew_tasks

    def create_the_society(self, task: str):
        # creates the smaller agents in the Mind
        society_of_minds = Agent(
            role='Mind Creator',
            goal='Create smaller process to achieve a complex task',
            verbose=False,
            memory=True,
            backstory=(
                "You are the creator of Mind. Each mind is made of many smaller processes which we call agents. "
                "You know that each mental agent by itself can only do some simple thing that needs no mind or thought at all."
                "Yet when we join these agents in societies, in certain very special ways, this leads to intelligence. Your "
                "job is to create a series of agents based on a provided complex task."),
            tools=[],
            allow_delegation=True
        )

        # creates the tasks for the agents
        society_of_minds_task = Task(
            description=(
                "{task}"
            ),
            expected_output='A list of agents with their name, role, goal, backstory, task and task output in a JSON '
                            'format.Only output the JSON. Keys in the JSON must be lower case and named as agent_name,role,'
                            'goal, backstory,task and taskoutput Do not add anything else.',
            tools=[],
            agent=society_of_minds,
            output_json=AgentList
        )

        crew = Crew(
            agents=[society_of_minds],
            tasks=[society_of_minds_task],
            verbose=False,
            process=Process.sequential  # Optional: Sequential task execution is default
        )
        agents = crew.kickoff(inputs={'task': task})
        agents = ast.literal_eval(agents)
        print(agents)
        crew_agents, crew_tasks = self.create_agent_tasks(agents['agents'])
        return crew_agents, crew_tasks

# if __name__ == "__main__":
#     mymind = TheMind()
#     task = "Create a powerpoint to explain the impact of technology on climate."
#     agents = mymind.create_the_society(task)
#     print(agents)
