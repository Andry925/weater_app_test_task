from pydantic import BaseModel, Field, field_validator
import re


class CityRequestSchema(BaseModel):
    cities: list[str] = Field(min_length=1, max_length=70)

    @field_validator('cities')
    @classmethod
    def validate_city(cls, cities):
        pattern = re.compile(r'^[^\d\W]+$', re.UNICODE)
        for city in cities:
            if len(city) < 3:
                raise ValueError("Each city must be at least 3 characters long")
            if not pattern.match(city):
                raise ValueError(f"City '{city}' contains numbers or special characters, which are not allowed.")

        return cities
