"""
Author: Rajib Deb
Date: 02/10/2024
Description: This module creates the crew objects with all the required agents and tasks
"""
import os

from crewai import Crew
from dotenv import load_dotenv

from crew_ai_crews.agents import MasterChef
from crew_ai_crews.tasks import ExtractIngredientsFromImage
from grandma_story.grandma_agents import GrandmaAgents
from grandma_story.story_tasks import CreateStories

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


class GrandmaCrew():
    """
    The crew which crafts the story. It is a crew of a single grandma agent
    """
    def __init__(self, idea):
        agents = GrandmaAgents(idea=idea)
        self.craft_story = agents.craft_the_story()

    def kickoff(self):
        """
        Creating the crew with grandma
        :return:
        """
        tasks = CreateStories()
        crew = Crew(
            agents=[self.craft_story],
            tasks=[tasks.craft_story(self.craft_story)],
            verbose=True
        )
        result = crew.kickoff()
        return result
