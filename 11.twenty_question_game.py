import os

from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

player1 = Agent(
    role="Martin",
    goal="You will guess the name of a personality",
    backstory="""Your name is Martin. You are playing the 20 question game with your friend Ravi and Shamik. In this game 
           you will think of a famous personality and share with Shamik. Ravi needs to guess the name, NEVER share the personality 
           name with Ravi.
            """,
    verbose=True,
    allow_delegation=False,
    memory = True
)

player2 = Agent(
    role="Shamik",
    goal="Answer only YES or NO to questions about about the personality",
    backstory="""Your name is Shamik. You are playing the 20 question game with your friend Martin and Ravi. Martin will share the name 
    of the personality with you. Ravi will ask 20 questions to you one by one about the personality that Martin shared with you. You need to answer YES or NO to the questions. 
    Through these 20 questions, Ravi will try to guess the name of the personality. DO NOT share the name of the 
    personality with Ravi.
            """,
    verbose=True,
    allow_delegation=True,
    memory = True
)

player3 = Agent(
    role="Ravi",
    goal="Ask 20 questions about the person and guess the name of the person",
    backstory="""Your name is Ravi. You are playing the 20 question game with your friend Shamik and Martin. 
    In this game you will ask 20 closed questions about that personality which 
    can be answered 'YES' or 'NO' . Only Shamik will answer YES or NO for those questions.
    Through these 20 questions, you should be able to identify the name of the personality. Ask the question one by one and wait
    for Shamik to answer before you ask next question. After all the questions are answered, you must try to 
    guess the name of the persoanlity.
            """,
    verbose=True,
    allow_delegation=True,
    memory = True
)

identification_task= Task(description="""You will identify the name of a personality
""", expected_output="name of a personality",agent=player1)

question_task = Task(description="""You will answer YES or NO when a question is asked about the personality
""", expected_output="answer about the personality",agent=player2)

answer_task = Task(description="""you will ask the question about the personality and guess the name of the personality 
through 20 questions only.
""", expected_output="name of the personality",agent=player3)

crew = Crew(
    agents=[player1, player2,player3],
    tasks=[identification_task,question_task, answer_task],
    verbose=2,  # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
