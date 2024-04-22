# imports
import os
from uuid import uuid4

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tracers.context import tracing_v2_enabled
from langchain_groq import ChatGroq
from crewai_tools import SerperDevTool

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

unique_id = uuid4().hex[0:8]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"Crew AI - {unique_id}"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get('LANGSMITH_API_KEY')  # Update to your API key


# Keys
os.environ["SERPER_API_KEY"] = os.environ.get('serapi_key')
os.environ["GROQ_API_KEY"] = os.environ.get('groq_key')
# Tools
wikipedia=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
serper = SerperDevTool()
# Groq

Groq = ChatGroq(
   temperature=0.7,
   model_name='llama3-70b-8192'
)

# agents1



jornalista = Agent(
  role='Historiador e jornalista Esportivo pesquisador sobre futebol Brasileiro',
  backstory='Você possue larga experiência em pesquisas sobre carreiras de jogadores do futebol brasileiro, possue vários livros escritos.',
  goal='Realiza pesquisas sobre o histórico da carreira dos jogadores de futebol do Brasil',
  llm=Groq,
  verbose=True
  )

# angents3
editor = Agent(
    role='Editor e Crítico Esportivo',
    backstory='Você constrói críticas jornalísticas e editoriais',
    goal='Escrever matérias jornalísticas e críticas detalhada',
    llm=Groq,
    verbose=True

)

# agenst4
revisor = Agent(
    role='Revisor de textos',
    backstory='Você é um jornalista revisor de textos',
    goal='Revisa texto final para publicação',
    llm=Groq,
    verbose=True

)

# agenst5
tradutor = Agent(
    role='tradutor de textos',
    backstory='Você é um tradutor de textos para o português',
    goal='Traduzir o texto do revisor para a publicação',
    llm=Groq,
    verbose=True

)

# task1
carreira = Task(
    description='Pesquisa na página da Wikipedia em pt-BR sobre o histórico sobre a carreira, conquistas e polêmicas do jogador Gabriel Barbosa, o Gabigol.',
    expected_output='Através de uma pesquisa na página da Wikipedia em pt-BR, vai extrair uma descrição dos principais fatos do histórico da carreira do jogador Gabriel Barbosa, o Gabigol. Ênfase especial nas conquistas e polêmicas na carreira',
    agent=jornalista,
    tools=[wikipedia]
)

# task3
contexto_fraude_antidoping=Task(
    description='Pesquisar na internet nas fontes de notícias no Brasil e em português sobre a tentativa de fraude do antidoping do jogador Gabriel Barbosa, o Gabigol em 2024',
    expected_output='Resultado das notícias do contexto da tentativa de fraude ao antidoping do Gabigol e as Últimas notícias sobre o caso.',
    agent=jornalista,
    tools=[serper]
)

# task4
crítica=Task(
    description='Escrever uma matéria completa e uma crítica detalhada sobre o caso de fraude do antidoping do jogador Gabriel Barbosa, o Gabigol, em 2024',
    expected_output='Levantamento de questões sobre o caso e a criação de uma matéria e crítica detalhada sobre o caso da tentativa fraude do antidoping do jogador Gabriel Barbosa, o Gabigol',
    agent=editor,
    context=[carreira, contexto_fraude_antidoping]
)

# task5
revisão=Task(
    description='Fazer a revisão final do texto do crítico para publicação',
    expected_output='Entrega do texto final na íntegra revisado para publicação',
    agent=revisor,
    context=[carreira,contexto_fraude_antidoping,crítica]
)

tradução=Task(
    description='Fazer a tradução do texto final para o português',
    expected_output='Receber o texto final na íntegra revisado em pt-br',
    agent=tradutor
    )

# Assemble a crew
crew = Crew(

    agents=[jornalista, editor, revisor, tradutor],
    tasks=[carreira, contexto_fraude_antidoping, crítica, revisão, tradução],
    full_output=True,
    process=Process.sequential,
    verbose=2,
    output_log_file=True

)
crew.kickoff()
print(f"""
    Task completed!
    Task: {revisão.output.description}
    Output: {tradução.output.raw_output}
""")
with tracing_v2_enabled(project_name=f"Crew AI - {unique_id}"):
    result = crew.kickoff()

print(result)
