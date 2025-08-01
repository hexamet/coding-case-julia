from fastapi import APIRouter, Body, Depends, HTTPException
from pydantic import BaseModel
from geocoding import (
    PhotonCityLocation
)
from sqlalchemy.orm import Session
from database import get_session, add_city_to_database
from database_model import City
from sqlalchemy.exc import OperationalError

router = APIRouter()

class CityURL(BaseModel):
    short_url: str
    
class CityCoordinate(BaseModel):
    latitude: float
    longitude: float
    

@router.post("/short-location", response_model=CityURL, tags=["city"])
def short_location(
                   city_name:str=Body(default="München", embed=True),
                   geo_locator: PhotonCityLocation = Depends(PhotonCityLocation), 
                   session:Session = Depends(get_session)
    )-> CityURL:
    #TODO: 
    # * add pattern to check for digits in names
    # * add checking if city string is a real city and not a village or region
    # * add sth when one city name returns multiple results
       
    city_geo_data = geo_locator.get_geo_data(city_name)
    
    if not city_geo_data:
        raise HTTPException(status_code=500, detail=f"Cannot find city: {city_name}")
    try:
        add_city_to_database(city_geo_data, session)
    except OperationalError:
        raise HTTPException(status_code=503, detail="Cannot connect to database")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

    my_city_url = CityURL(short_url=f"http://localhost:8000/{city_geo_data.id}")

    return my_city_url

@router.get("/{short}", response_model=CityCoordinate, tags=["city"])
def get_city_from_short(short:str, session:Session = Depends(get_session)) -> CityCoordinate:
    data = session.query(City).filter(City.id == short).first()
    
    if not data:
        raise HTTPException(status_code=404, detail=f"Short url not found")
    
    city_coords  = CityCoordinate(latitude=data.lat, longitude=data.lng)
    return city_coords
    
        

