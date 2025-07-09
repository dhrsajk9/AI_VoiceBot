from dotenv import load_dotenv
load_dotenv()

## Setup Groq API Key
import os

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

import base64

## Convert image to required format
# image_path="acne.jpg"
def encode_image(image_path):
    image_file=open(image_path, "rb") #Read binary
    return base64.b64encode(image_file.read()).decode('utf-8')

## Setup Multimodal LLM
from groq import Groq

query="Is something wrong with my skin?"
model ="meta-llama/llama-4-scout-17b-16e-instruct"

def analyze_image_with_query(query, model, encoded_image):
    client=Groq()  
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text", 
                    "text": query
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_image}",
                    },
                },
            ],
        }]
    chat_completion=client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content