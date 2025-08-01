import os
import requests
from typing import Any
from database_model import City
import hashlib
from fastapi import HTTPException

def get_uid(value:str)->str:
    hash_obj = hashlib.sha256()
    hash_obj.update(value.encode("ascii", "ignore"))
    return hash_obj.hexdigest()[0:6]
     
class PhotonCityLocation():
    def __init__(self):
        self.__city_name: str = ""
        self.__geo_api_url: str = os.getenv("GEO_API", "")
        self.__geo_api_lang: str = os.getenv("GEO_LANG","")
        self.__geo_api_limit:str = os.getenv("GEO_LIMIT","")
        self.__city:City|None = None
        
    def __get_request_params(self) -> dict[str, str]:
        params: dict[str,str] = {
            "q": self.__city_name.lower(),
            "lang": self.__geo_api_lang,
            "limit": self.__geo_api_limit,
        }
        params = {k: v for k, v in params.items() if v}
        
        return params
    
    def __get_geo_data_from_api(self,timeout:int = 60) -> dict[str,Any]:
        try:
            if not self.__geo_api_url:
                raise ValueError("No geo api url defined")
            response= requests.get(self.__geo_api_url, params=self.__get_request_params(), timeout=timeout)
            response.raise_for_status()
            return response.json()        
        except ValueError as e:
            raise HTTPException(status_code=500, detail=f"{e}")
        except requests.HTTPError as e:
            raise HTTPException(
                    status_code= response.status_code,
                    detail = f"Error connecting to geo api: {e}"
                )
    
    def __prarse_from_json(self, geo_json: dict[str,Any]) -> City|None:
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
                        self.__city = City(
                            city=city_name, 
                            lng=coordinates[0], 
                            lat=coordinates[1], 
                            id=get_uid(city_name)
                        )
                        # only return first result
                        return self.__city
                        
        return None
    
    def get_geo_data(self, city_name:str) -> City|None:
        self.__city_name = city_name
        geo_api_response = self.__get_geo_data_from_api()
        return self.__prarse_from_json(geo_api_response)
    
            
    
    
