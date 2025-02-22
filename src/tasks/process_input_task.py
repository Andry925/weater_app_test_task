import asyncio
import json

from celery_worker import celery_app
from decouple import config
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from utils.weather_api_util import get_weather
from utils.weather_api_util import save_weather_data

OPENAI_API_KEY = config('OPENAI_API_KEY')
WEATHER_API_KEY = config("WEATHER_API_KEY")


@celery_app.task(name='process_weather_task', bind=True)
def process_input(self, city_lists):
    current_task_id = self.request.id
    process_request = asyncio.run(get_weather(city_lists, WEATHER_API_KEY))
    saved_files = asyncio.run(save_weather_data(process_request, task_id=current_task_id))

    return {
        "weather_data": process_request,
        "saved_files": saved_files
    }


@celery_app.task(name='process_input_task')
def create_llm_prompt(city_lists):
    chatgpt_template = f"""
        You are a multilingual language model specializing in city name translation and normalization
        Given the list of cities:
        {city_lists}
        1. Translate all city names to English, regardless of their original language.
        2. Normalize city names (e.g., 'Киев' → 'Kyiv', 'Londn' → 'London').
        3. Translate the city name in English if the city name is not in English
        4. Return a JSON response with 'cities' as a key and the corrected list as values.
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
