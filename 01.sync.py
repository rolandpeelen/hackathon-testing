# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %%
from openai import OpenAI
import os
import base64
import json

client = OpenAI()

with open("./01.html", "rb") as html_file:
    html01 = html_file.read()
with open("./02.html", "rb") as html_file:
    html02 = html_file.read()
with open("./image.png", "rb") as image_file:
    base64_utf8_str = base64.b64encode(image_file.read()).decode('utf-8')
    image01 = f'data:image/png;base64,{base64_utf8_str}'
with open("./image02.png", "rb") as image_file:
    base64_utf8_str = base64.b64encode(image_file.read()).decode('utf-8')
    image02 = f'data:image/png;base64,{base64_utf8_str}'

completion = client.chat.completions.create(
    model="gpt-4-vision-preview",
    max_tokens=4096,
    messages=[
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": """
            You are a sales consultant / solutions engineer. You help companies
            create demos of their products. Their products are software
            applications that are built using web technologies. You are going
            to help someone make a demo. You will be presented with a prompt
            that holds information about the product the client wants to
            present, about their prospect, and a rough description on what the
            product does. You will then receive a screenshot of the page, with
            the corresponding HTML structure. It's simplified. We
            only have the tags, and every element has it's
            own id, which is inside of the html's 'i' tag. I want you to think
            of 3 places you'd possibly click next, given our customers prompt.
            Then I want you to match each of them to a place in the HTML
            structure. The response we want is a JSON object, with the
            following schema (psuedo-code)
            ``` 
                type guess = { 
                    id: <id-to-click>,
                    action: <what would happen when you click there>
                }; 
                type guesses = {01: guess, 02: guess, 03: guess} 
                type response = {
                    description: <summary of what this page is for>, 
                    guess: guesses, 
                }
            ```

            - Make sure the element to click is visible in the screenshot!
            - Return only the 3 guesses in the correct format
            """,
                }
            ],
        },
        # {
            # "role": "user",
            # "content": [
                # {"type": "image_url", "image_url": f"{image01}"},
                # {
                    # "type": "text",
                    # "text": f"""
                # The product is a web application that is essentially a CMS for 3d
                # product configurators. You can upload 3d models, textures, and
             # environments. You can create materials, and then you can combine them
             # together in what we call a 'konfig', which allows you to add options,
             # combine the options into steps, add pricing, SKU's, etc.
             
             # I want to create a demo that shows how to upload an environment.

             # Here is the html: {html01}
             # """,
                # },
            # ],
        # },
        {
            "role": "system",
            "content": """
         ```json
         {
              "description": "The web app screen shows tabs for 'Konfigs', 'Materials', 'Textures', 'Meshes', 'Previews', and 'Environments' at the top. There are also two product configuration cards; one for 'Bold' and another for 'ZEE', showing preview images and view counts.",
              "guess": {
                "01": {
                  "id": "70",
                  "action": "Navigates to the Environments section where you can manage and upload environment assets for product configurators."
                },
                "02": {
                  "id": "c1",
                  "action": "Initiates the creation process for a new item, possibly an environment based on the demo requirement."
                },
                "03": {
                  "id": "f9",
                  "action": "Puts focus on the search input field to filter or search for specific environments or other assets."
                }
              }
            }
         ```
         """,
        },
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": f"{ image02 }"},
                {
                    "type": "text",
                    "text": f"""
                             I clicked on id "70". That took me to this page.

                             In a demo with this initial prompt:

                                "The product is a web application that is essentially a CMS for
                                3d product configurators. You can upload 3d models, textures,
                                and environments. You can create materials, and then you can
                                combine them together in what we call a 'konfig', which allows
                                you to add options, combine the options into steps, add
                                pricing, SKU's, etc.
                                I want to create a demo that shows how to upload an environment."
 
                             Where should the user click next?

                             Here is the html: {html02}
                             """,
                },
            ],
        },
    ],
)
print(completion.choices[0].message.content)
