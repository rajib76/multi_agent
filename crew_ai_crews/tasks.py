"""
Author: Rajib Deb
Descriptions: Defines all the tasks that will be used by the agents
"""
from crewai import Task
from textwrap import dedent


class ExtractIngredientsFromImage:
    def get_ingredients(self, agent):
        """
        This task is for the food connoisseur agent which will analyze the image of the food item
        and extract ingredients out of it.
        :param agent: The food connoisseur agent
        :return: Returns the task object
        """
        task = Task(
            description=dedent(f"""
            Analyze an image of a food item and extract ingredients of the food
"""), agent=agent
        )

        return task

    def cooking_instruction(self, agent):
        """
        The task to be used by the chef
        :param agent: The master chef agent
        :return: Returns the task of the chef
        """
        task = Task(
                description=dedent(f"""
                Instruct how to cook a healthy food item based on the provided ingredients
    """), agent=agent
            )

        return task
