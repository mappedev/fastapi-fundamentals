''' Python imports '''
from typing import Optional

''' Pydantic imports '''
from pydantic import BaseModel

''' FastAPI imports '''
from fastapi import Body, FastAPI

app = FastAPI()


''' Models '''
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None


@app.get('/')
def home():
    return {'Hello': 'World'}

''' Request and response body '''
@app.post('/persons')
def create_person(person: Person = Body(...)):
    return person
