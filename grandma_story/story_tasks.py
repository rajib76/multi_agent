"""
Author: Rajib Deb
Descriptions: Defines all the tasks that will be used by the agents
"""
from crewai import Task
from textwrap import dedent


class CreateStories:
    def craft_story(self, agent):
        """
        This task is for grandma to craft the story
        :param agent: The grandma agent
        :return: Returns the task object
        """
        task = Task(
            description=dedent(f"""
            Craft a kid story based on an initial idea that will teach the kids good values and make them a better human
"""), agent=agent
        )

        return task
