import os
import requests
from typing import Any
from database_model import City
import hashlib
from fastapi import HTTPException

GEO_API = os.getenv("GEO_API", "")
GEO_LANG = os.getenv("GEO_LANG","")
GEO_LIMIT = os.getenv("GEO_LIMIT","")


def get_uid(value:str)->str:
    hash_obj = hashlib.sha256()
    hash_obj.update(value.encode("ascii", "ignore"))
    return hash_obj.hexdigest()[0:6]
     
def get_url_and_params_for_request(city:str) -> tuple[str, dict[str, Any]]:
    if not GEO_API:
        raise ValueError("No geo api defined")
    
    params = {
        "q": city.lower(),
        "lang": GEO_LANG,
        "limit": GEO_LIMIT,
    }
    params = {k: v for k, v in params.items() if v}
    
    return GEO_API, params
    
def request_from_geo_api(url: str, params:dict[str, Any], timeout:int=60) -> dict[str, Any] :
    try:
        response= requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as e:
        raise HTTPException(
            status_code= response.status_code,
            detail = f"error calling geo api: {e}"
                            )
    
def parse_from_json(geo_json:dict[str, Any])->  City|None:
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
                    city = City(
                        city=city_name, 
                        lng=coordinates[0], 
                        lat=coordinates[1], 
                        id=get_uid(city_name)
                    )
                    return city
    return None
                  
def get_geo_data(city_name:str)-> City:
    url, params = get_url_and_params_for_request(city_name)
    geo_response = request_from_geo_api(url, params)
    city_geo_data = parse_from_json(geo_response)
    return city_geo_data                    
            
    
    
