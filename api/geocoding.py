import os
import requests
from typing import Any
from dataclasses import dataclass

GEO_API = os.getenv("GEO_API", "")
GEO_LANG = os.getenv("GEO_LANG","")
GEO_LIMIT = os.getenv("GEO_LIMIT","")

@dataclass
class City():
    name:str
    lat:float
    lng: float
    

def build_request(city:str) -> str:
    geo_request:str = ""
    if GEO_API:
        geo_request = f"{GEO_API}/?q={city.lower()}"
    else:
        raise ValueError("No geo api defined")
    
    if GEO_LANG:
        geo_request +=f"&lang={GEO_LANG}"
    if GEO_LIMIT:
        geo_request += f"&limit={GEO_LIMIT}"
    
    return geo_request
    
def get_geo_response(geo_request: str) -> dict[str, Any] :
    response= requests.get(geo_request, timeout=60)
    if response.status_code == 200:
        return response.json()
    else:
        raise ConnectionError(f"No response from request: {geo_request}")
    
def parse_from_json(geo_json:dict[str, Any])->  City:
    # we assume the geo json looks like this example:
    # https://photon.komoot.io/api/?q=berlin&limit=1
    
    # only extract geo coordinates
    if features:=geo_json.get("features"):
        for feature in features:
            city_name:str = ""
            if properties := feature.get("properties"):
                city_name = properties.get("name", "")
            if geometry:=feature.get("geometry"):
                if coordinates := geometry.get("coordinates"):
                    city = City(city_name, coordinates[0], coordinates[1])
                    return city
    return City("", -1, -1)
                    
                    
            
    
    
