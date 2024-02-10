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

load_dotenv()
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


class MasterChefCrew():
    """
    The master chef crew consisting of the food connoisseur and the chef
    """
    def __init__(self, url):
        agents = MasterChef(url=url)
        self.extract_agent = agents.get_recipe_from_image()
        self.instruct_agent = agents.instruct_to_cook_dish()

    def kickoff(self):
        """
        Creating the crew with the two agents
        :return:
        """
        tasks = ExtractIngredientsFromImage()
        crew = Crew(
            agents=[self.extract_agent, self.instruct_agent],
            tasks=[tasks.get_ingredients(self.extract_agent), tasks.cooking_instruction(self.instruct_agent)],
            verbose=True
        )
        result = crew.kickoff()
        return result
