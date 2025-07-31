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
    

@router.post("/short-location", response_model=CityURL, tags=["city"])
def short_location(city:str=Body(default="München", embed=True), database:Session = Depends(get_database))-> CityURL:
    #TODO: 
    # * add pattern to check for digits in names
    # * add checking if city string is a real city and not a village or region
    # * add sth when one city name returns multiple results
    try:
        geo_response = get_geo_response(build_request(city))
        response_city = parse_from_json(geo_response)
    except ConnectionError:
        raise HTTPException(status_code=500,detail="sht went wrong")
    except HTTPError:
        raise HTTPException(status_code=500, detail="Cannot connect to geo api")
    
    try:
        database.add(response_city)
        database.commit()
        database.refresh(response_city)
    except Exception:
        raise HTTPException(status_code=500, detail="Error connecting to database")
    
    my_city_url = CityURL(short_url=f"http://localhost:8000/{response_city.id}")
    
    return my_city_url