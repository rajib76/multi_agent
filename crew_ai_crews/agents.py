"""
Author: Rajib Deb
Date: 02/01/2024
Description: This module wraps all the agents that we will use for our use case
"""
from textwrap import dedent

from crewai import Agent

from crew_ai_crews.tools import ExtractIngredients


class MasterChef():
    """
    This class wraps all the agents that we will use for our use case
    """
    def __init__(self,url):
        self.module = __name__
        self.url = url

    def get_recipe_from_image(self):
        """
        This creates the agent which can extract ingredients used to prepare a food item. This image will
        use a tool to extract the information from the image. The tool uses gpt-4-v-preview model
        :return: Returns the agent object
        """
        agent = Agent(
        role='Food Connoisseur',
        goal='Extract ingredients of a food item looking at the image.',
        backstory=dedent("""As a food connoisseur, you have extensive experience is exploring delicious food items.
        You are adept at identifying the food ingredients by looking at the provided url of the image of food items.
        <url>
        {url}
        """.format(url=self.url)
        ),
        tools=[ExtractIngredients.extract_ingredient],
        verbose=True,
        allow_delegation=False)

        return agent

    def instruct_to_cook_dish(self):
        """
        This creates the agent which can instruct how to cook the food item based on the ingredients extracted.
        This uses its parametric knowledge to prepare the dish.
        :return: Returns the agent object
        """
        agent = Agent(
        role='Master Chef',
        goal='Instruct how to cook a dish based on the provided ingredients of the food',
        backstory=dedent("""As a famous chef, you have extensive experience is making delicious food items.
        You are adept at providing instructions on how to cook a healthy dish with the ingredients provided."""
        ),
        verbose=True,
        allow_delegation=False)

        return agent
