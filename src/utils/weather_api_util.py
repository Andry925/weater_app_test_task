import asyncio
import json
import os

import aiofiles
import aiohttp


async def fetch_weather(session, city, api_key):
    try:
        api_url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&alerts=yes'
        async with session.get(api_url) as response:
            response.raise_for_status()
            return {city: await response.json()}

    except aiohttp.ClientResponseError as error:
        return {city: {"error": f"HTTP ERROR for {city}: {error.status}"}}
    except aiohttp.ClientError as error:
        return {city: {"error": f"Request error: {str(error)}"}}


async def get_weather(cities, api_key):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_weather(session, city, api_key) for city in cities]
        results = await asyncio.gather(*tasks)
        return results


async def process_data_to_required_format(results):
    processed_data = {"status": "completed", "results": {}}

    for city_data in results:
        city_name = list(city_data.keys())[0]
        city_info = city_data[city_name]
        temperature = city_info["current"]["temp_c"]
        description = city_info["current"]["condition"]["text"].lower()
        tz_id = city_info["location"]["tz_id"]
        continent = tz_id.split("/")[0]

        if continent not in processed_data["results"]:
            processed_data["results"][continent] = []

        processed_data["results"][continent].append({
            "city": city_name,
            "temperature": temperature,
            "description": description
        })

    return processed_data


async def save_weather_data(weather_results, task_id):
    processed_data = await process_data_to_required_format(weather_results)
    file_paths = {}
    for region, cities_data in processed_data["results"].items():
        region_folder = f"weather_data/{region}"
        file_path = f"{region_folder}/task_{task_id}.json"
        if not os.path.exists(region_folder):
            os.makedirs(f"{region_folder}")

        async with aiofiles.open(file_path, 'w') as outfile:
            json_data = {"results": cities_data}
            await outfile.write(json.dumps(json_data, indent=4))
            file_paths[region] = file_path
    return file_paths
