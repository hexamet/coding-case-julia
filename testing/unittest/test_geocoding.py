import pytest
import geocoding

test_set:list[tuple[str,str]] = [
    ("München", "aebcfb"),
    ("Niederroßla", "aa7a1c"),
    ("1234", "03ac67"),
    ("","e3b0c4")
]
    
@pytest.mark.parametrize("value, result", test_set)
def test_get_uid(value:str, result:str):
    short_id:str = geocoding.get_uid(value)
    assert short_id == result