import os
import openai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # поиск файла .env в директории проекта


async def chatgpt_mes(message):
    openai.api_key = (os.getenv('GPT_TOKEN'))
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message,
        temperature=0.0,
        max_tokens=1500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["You:"]
    )
    return response['choices'][0]['text']
