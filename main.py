''' Python imports '''
from typing import Optional
from enum import Enum

''' Pydantic imports '''
from pydantic import BaseModel, Field

''' FastAPI imports '''
from fastapi import Body, FastAPI, Query, Path

app = FastAPI()


''' Models '''
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class Person(BaseModel):
    first_name: str = Field(
        default=...,
        min_length=1,
        max_length=50,
    )
    last_name: str = Field(
        default=...,
        min_length=1,
        max_length=50,
    )
    age: int = Field(
        default=...,
        gt=0,
        le=115,
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
    )
    is_married: Optional[bool] = Field(
        default=False,
    )


class Location(BaseModel):
    city: str
    state: str
    country: str


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
        default=..., # required
        ge=0,
        title='Person age',
        description='Person age (21), It is required!',
    ),
):
    return {name: age}

''' Validations path parameters'''
@app.get('/persons/{person_id}')
def get_person(
    person_id: int = Path(
        default=...,
        ge=1,
        title='Person ID',
        description='Person ID (1), It is required!'
    ),
):
    return {person_id: 'It exists!'}

''' Validations request body '''
@app.put('/persons/{person_id}')
def update_person(
    person_id: int = Path(
        default=...,
        ge=1,
        title='Person ID',
        description='Person ID (1), It is required!',
    ),
    person: Person = Body(default=...),
    location: Location = Body(default=...),
):
    # return person.dict() & location.dict()
    results = person.dict()
    results.update(location.dict())
    return results

''' Validations models '''
