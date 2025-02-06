from celery import chain
from decouple import config
from fastapi import APIRouter, status

from schemas.cities_request_schema import CityRequestSchema
from tasks.process_input_task import create_llm_prompt, process_input

router = APIRouter(prefix="/api/v1", tags=["weather"])
WEATHER_API_KEY = config("WEATHER_API_KEY")


@router.post("/weather", status_code=status.HTTP_202_ACCEPTED)
async def create_weather_request(city_request: CityRequestSchema):
    task_chain = chain(
        create_llm_prompt.s(city_request.cities) |
        process_input.s()
    )

    result = task_chain.apply_async()
    return {
        "message": "Weather request is being processed",
        "task_id": result.id}
