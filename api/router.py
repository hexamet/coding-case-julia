from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from geocoding import (
    get_geo_data
)
from sqlalchemy.orm import Session
from database import get_database, add_city_to_database
from database_model import City
from sqlalchemy.exc import OperationalError

router = APIRouter()

class CityURL(BaseModel):
    short_url: str
    
class CityCoordinate(BaseModel):
    latitude: float
    longitude: float
    

@router.post("/short-location", response_model=CityURL, tags=["city"])
def short_location(city_name:str=Body(default="München", embed=True), database:Session = Depends(get_database))-> CityURL:
    #TODO: 
    # * add pattern to check for digits in names
    # * add checking if city string is a real city and not a village or region
    # * add sth when one city name returns multiple results
    # * change get_geo_data to servic class
       
    city_geo_data = get_geo_data(city_name=city_name)
    
    if not city_geo_data:
        raise HTTPException(status_code=500, detail=f"Cannot find city: {city_name}")
    try:
        add_city_to_database(city_geo_data, database)
    except OperationalError:
        raise HTTPException(status_code=503, detail="Cannot connect to database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unknown error. {e}")

    my_city_url = CityURL(short_url=f"http://localhost:8000/{city_geo_data.id}")

    return my_city_url

@router.get("/{short}", response_model=CityCoordinate, tags=["city"])
def get_city_from_short(short:str, database:Session = Depends(get_database)) -> CityCoordinate:
    data = database.query(City).filter(City.id == short).first()
    
    if not data:
        raise HTTPException(status_code=404, detail=f"Short URL not found")
    
    city_coords  = CityCoordinate(latitude=data.lat, longitude=data.lng)
    return city_coords
    
        

