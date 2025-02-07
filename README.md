# Asynchronous Weather Data Retrieval Task

This is an asynchronous weather data retrieval application.

## Overview

This system accepts a list of cities from the user via an HTTP POST request, fetches weather data for each city using an external API, and saves the processed results in a specific format for further analysis.

## How to Run the Program

1. Fill in the `.env` file with your configuration data:
   - Provide your `OPENAI_API_KEY`, as the application uses LangChain to process the list of cities.
   - The external free weather API key will be included in the `.env` file for ease of access by the technical team. But you can obtain your own free key via this link [WeatherAPI](https://www.weatherapi.com/signup.aspx).

2. Run the project using Docker:
   ```sh
   docker-compose up --build
   ```
   Wait for the services to start.

## Features Implemented

1. Fully implemented functionality as per the requirements.
2. Efficient data processing using LangChain, with city list validation via LLM.
3. Robust error handling and validation for various scenarios.
4. Asynchronous execution using Celery for handling API calls efficiently.
5. Support for multiple external API keys.
6. Docker and Docker Compose configurations for seamless deployment.

## API Documentation

You can access the API documentation via Swagger at:
[Swagger Documentation](http://127.0.0.1:8000/docs)

## Limitations

1. Automated tests have not been implemented yet.
