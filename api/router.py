from fastapi import APIRouter,Body 
from typing import Annotated
from pydantic import BaseModel, Field
from geocoding import (
    get_geo_response, 
    build_request,
    parse_from_json
)


router = APIRouter()

class CityURL(BaseModel):
    short_url: str
    

@router.post("/short_location", response_model=City_URL, tags=["city"])
def short_location(city:str=Body(default="München", embed=True))-> str:
    #TODO: add pattern to check for digits in names
    my_city_url = City_URL(short_url=city)
    geo_response = get_geo_response(build_request(city))
    response_city = parse_from_json(geo_response)
    print(response_city)
    
    return my_city_url