import json
import os

import aiofiles
from celery import chain
from celery.result import AsyncResult
from decouple import config
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from schemas import cities_request_schema
from tasks.process_input_task import create_llm_prompt, process_input

router = APIRouter(prefix="/api/v1", tags=["weather"])
WEATHER_API_KEY = config("WEATHER_API_KEY")


@router.post("/weather", status_code=status.HTTP_202_ACCEPTED)
async def create_weather_request(city_request: cities_request_schema.CityRequestSchema):
    try:
        task_chain = chain(
            create_llm_prompt.s(city_request.cities) |
            process_input.s()
        )

        result = task_chain.apply_async()
        return {
            "message": "Weather request is being processed",
            "task_id": result.id}
    except Exception as e:
        return {"message": str(e)}


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_status(task_id: str):
    try:

        task = AsyncResult(task_id)
        if not task.ready():
            return JSONResponse(
                status_code=202,
                content={
                    "task_id": task_id,
                    "status": task.state})

        if task.state == "FAILURE":
            return JSONResponse(
                status_code=500,
                content={
                    "task_id": task_id,
                    "status": "Failed",
                    "error": str(
                        task.result)})
        result = task.result
        saved_files = result.get("saved_files")
        return {
            "task_id": task_id,
            "status": "Success",
            "saved_files": saved_files
        }
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Task ID '{task_id}' not found.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task status: {str(e)}")


@router.get("/tasks/results/{region}", status_code=status.HTTP_200_OK)
async def get_task_results(region: str):
    try:
        json_response = []
        region_folder = f"weather_data/{region}"
        if not os.path.exists(region_folder):
            raise HTTPException(
                status_code=404,
                detail=f"Such region does not exist")
        all_files = os.listdir(region_folder)
        for file in all_files:
            file_path = os.path.join(region_folder, file)
            async with aiofiles.open(file_path, 'r') as infile:
                content = await infile.read()
                json_response.append(json.loads(content))
        return {"region": region, "tasks": json_response}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Region '{region}' folder missing.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading files: {str(e)}")
