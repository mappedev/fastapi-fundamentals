''' Python imports '''
from typing import Optional

''' Pydantic imports '''
from pydantic import BaseModel

''' FastAPI imports '''
from fastapi import Body, FastAPI, Query

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

''' Validations query parameters '''
@app.get('/persons')
def get_persons(
    name: Optional[str] = Query(
        default='Anonymous',
        min_length=1,
        max_length=50,
        title='Person name',
        description= 'Person name (Mario)',
    ),
    age: int = Query(
        ..., # required
        ge=0,
        title='Person age',
        description='Person age (21)',
    ),
):
    return {name: age}
