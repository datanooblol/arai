from pydantic import BaseModel
from typing import Dict, Any
from functools import wraps
from datetime import datetime


def timelog(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        response = func(*args, **kwargs)
        time_elapsed = datetime.now() - start_time
        print('\x1b[6;37;42m'+'Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed)+'\x1b[0m')
        return response
    return wrapper

class Document(BaseModel):
    id:str = None
    page_content:str
    metadata:Dict[str, Any]
    type:str = None