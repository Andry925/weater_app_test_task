from pydantic import BaseModel, Field, field_validator


class CityRequestSchema(BaseModel):
    cities: list[str] = Field(min_length=1, max_length=70)

    @field_validator('cities')
    @classmethod
    def validate_city(cls, cities):
        if any(len(city) < 3 for city in cities):
            raise ValueError("Each city must be at least 3 characters long")
        return cities
