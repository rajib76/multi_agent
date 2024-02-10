"""
Author: Rajib Deb
Date: 02/10/2024
Description: Defines the tool to be used to understand the image of the food item
"""
import json

from langchain.tools import tool
from openai import OpenAI


class ExtractIngredients():
    @tool("Extract ingredients")
    def extract_ingredient(url: str):
        """
        Useful to extract ingredients from a food item image
        :param url:The image url
        :return:returns the response after extracting information from the image
        """
        print("url is ", url)
        # Sometimes the REACT agent extracts the url as {'url':<url>} and sometimes ar <url>
        # below check is to handle both situations
        try:
            image_url_json=json.loads(url)
            print("url keys are ", image_url_json.keys())
            image_url = image_url_json["url"]
        except ValueError as e:
            image_url =url
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract ingredients from the food item image"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url":image_url,
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        return response.choices[0]
