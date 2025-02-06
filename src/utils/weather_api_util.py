import asyncio

import aiohttp


async def fetch_weather(session, city, api_key):

    try:
        api_url = f'http://api.weatherapi.com/v1/current.json?key={
            api_key}&q={city}&alerts=yes'
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
        print(results)
        return results
