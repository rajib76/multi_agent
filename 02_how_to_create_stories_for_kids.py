"""
Author: Rajib Deb
Date: 02/10/2024
Description: This is the driver program that starts the MasterChef crew.
"""
# from grandma_story.grandma_stories import GrandmaCrew
#
# if __name__ == "__main__":
#     idea = "Unity is strength"
#     crew = GrandmaCrew(idea=idea)
#     result = crew.kickoff()
#     print(result)

# Author: Rajib Deb
# A simple example showing how langgraph works

from langgraph.graph import MessageGraph
from openai import OpenAI

from grandma_story.grandma_stories import GrandmaCrew


def craft_story(state):
    messages = state[-1]
    crew = GrandmaCrew(idea=messages)
    response = crew.kickoff()
    return response


def convert_to_speech(state):
    client = OpenAI()
    messages = state[-1]

    with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="alloy",
            input=messages,
    ) as response:
        response.stream_to_file("story.mp3")

    return response


workflow = MessageGraph()

# Define the nodes we will cycle between
workflow.add_node("craft_story", craft_story)
workflow.add_node("convert_to_speech", convert_to_speech)
workflow.set_entry_point("craft_story")
workflow.add_edge("craft_story", "convert_to_speech")
workflow.set_finish_point("convert_to_speech")

app = workflow.compile()

story_idea = "Unity is strength"
response = app.invoke(story_idea)
print("-----")
print(response[-1])
