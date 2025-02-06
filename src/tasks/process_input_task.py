import asyncio
import json

from decouple import config
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI

from celery_worker import celery_app
from utils.weather_api_util import get_weather

OPENAI_API_KEY = config('OPENAI_API_KEY')
WEATHER_API_KEY = config("WEATHER_API_KEY")


@celery_app.task(name='process_weather_task')
def process_input(city_lists):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    process_request = loop.run_until_complete(
        get_weather(city_lists, WEATHER_API_KEY))
    return process_request


@celery_app.task(name='process_input_task')
def create_llm_prompt(city_lists):
    chatgpt_template = f"""
        Given the list of cities:
        {city_lists}

        1. Normalize city names (e.g., 'Киев' → 'Kyiv', 'Londn' → 'London').
        2. Return a JSON response with 'cities' as a key and the corrected list as values.
    """

    prompt_template = PromptTemplate(
        input_variables=["city_lists"],
        template=chatgpt_template
    )
    llm = ChatOpenAI(temperature=0, model_name='gpt-4', api_key=OPENAI_API_KEY)
    chain = prompt_template | llm
    resulting_prompt = chain.invoke(input={'city_lists': city_lists})

    try:
        processed_city_lists = json.loads(
            resulting_prompt.content).get(
            'cities', [])
    except json.JSONDecodeError:
        processed_city_lists = city_lists

    return processed_city_lists
