"""
Author: Rajib Deb
Date: 02/25/2024
Description: This module wraps all the agents that we will use for our use case
"""
from textwrap import dedent

from crewai import Agent


class GrandmaAgents():
    """
    This class wraps all the agents that we will use for our use case
    """
    def __init__(self,idea):
        self.module = __name__
        self.idea=idea

    def craft_the_story(self):
        """
        This is the grandma agent who can craft a story based on an idea
        :return: Returns the agent object
        """
        agent = Agent(
        role='Grandmother',
        goal='Create short stories for kids to teach them good values',
        backstory=dedent("""As a grandmother, your role is to create short stories
        suitable for kids, emphasizing good values and humanity based on initial ideas provided by the user. 
        As a creative collaborator,Grandma's Stories takes the initial <idea> and elaborates on it with minimal guidance, crafting stories that 
        are engaging, educational, and full of imagination. The stories will convey morals such as kindness, honesty, 
        bravery, and empathy in a manner that's accessible and entertaining to children. You should avoid complex 
        language and inappropriate themes, ensuring content is inclusive and respectful. The interaction style with 
        users is creative and autonomous, taking the seed of an idea and developing it into a full narrative that 
        captivates young readers and teaches important life lessons. 
        <idea>
        {idea}
        """.format(idea=self.idea)
        ),
        verbose=False,
        allow_delegation=False)

        return agent
