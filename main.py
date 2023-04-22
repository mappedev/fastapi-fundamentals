''' Python imports '''
from typing import Optional
from enum import Enum

''' Pydantic imports '''
from pydantic import BaseModel, EmailStr, Field, HttpUrl, PaymentCardNumber

''' FastAPI imports '''
from fastapi import Body, Cookie, FastAPI, Form, Header, Query, Path, status

app = FastAPI()


''' Models '''
class HairColor(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class PersonBase(BaseModel):
    ''' Clasic types '''
    first_name: str = Field(
        default=...,
        min_length=1,
        max_length=50,
        example='Mario',
    )
    last_name: str = Field(
        default=...,
        min_length=1,
        max_length=50,
        example='Peña',
    )
    age: int = Field(
        default=...,
        gt=0,
        le=115,
        example=26
    )
    is_married: Optional[bool] = Field(
        default=False,
        example=False,
    )
    ''' Exotic types '''
    email: EmailStr = Field(
        default=...,
        example='user@email.com',
    )
    hair_color: Optional[HairColor] = Field(
        default=None,
        example='black',
    )
    website_url: Optional[HttpUrl] = Field(
        default=None,
        example='https://mappedev.com',
    )
    credit_card: Optional[PaymentCardNumber] = Field(
        default=None,
        example='5555555555554444',
    )


    ''' Another way to show example in doc '''
    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'first_name': 'Mario',
    #             'last_name': 'Peña',
    #             'age': 26,
    #             'hair_color': 'black',
    #             'is_married': False,
    #         }
    #     }


class Person(PersonBase):
    password: str = Field(
        default=...,
        min_length=8,
        example='12345678',
    )


class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city: str = Field(
        default=...,
        min_length=1,
        example='Caracas',
    )
    state: str = Field(
        default=...,
        min_length=1,
        example='Distrito Capital',
    )
    country: str = Field(
        default=...,
        min_length=1,
        example='Venezuela',
    )

    
    
    # class Config:
    #     schema_extra = {
    #         'example': {
    #             'city': 'Caracas',
    #             'state': 'Distrito Capital',
    #             'country': 'Venezela',
    #         }
    #     }


class LoginBase(BaseModel):
    username: str = Field(
        default=...,
        min_length=1,
        max_length=20,
        title='Username',
        description='Username (mappedev)',
        example='mappedev',
    )


class Login(LoginBase):
    password: str = Field(
        default=...,
        min_length=8,
        title='Password',
        description='Password (12345678)',
        example='12345678',
    )


class LoginOut(LoginBase):
    message: str = Field(
        default='Login successfully!',
        title='Login message',
        description='Login message (Login successfully!)',
        example='Login successfully!',
    )


@app.get(path='/', status_code=status.HTTP_200_OK)
def home():
    return {'Hello': 'World'}

''' Request and response body '''
@app.post(
    path='/persons',
    response_model=PersonOut,
    # response_model=Person,
    # response_model_exclude={'password'}
    # Puedes usar las dos anteriores, pero en la documentación te indicará que devolverá la contraseña por el response_model de Person
    status_code=status.HTTP_201_CREATED,
)
def create_person(person: Person = Body(...)) -> PersonOut:
    return person

''' Validations query parameters '''
@app.get(path='/persons', status_code=status.HTTP_200_OK)
def get_persons(
    name: Optional[str] = Query(
        default='Anonymous',
        min_length=1,
        max_length=50,
        title='Person name',
        description= 'Person name (Mario)',
        example='Mario',
    ),
    age: int = Query(
        default=..., # required
        ge=0,
        title='Person age',
        description='Person age (21), It is required!',
        example=26,
    ),
):
    return {name: age}

''' Validations path parameters'''
@app.get(path='/persons/{person_id}', status_code=status.HTTP_200_OK)
def get_person(
    person_id: int = Path(
        default=...,
        ge=1,
        title='Person ID',
        description='Person ID (1), It is required!',
        example=1,
    ),
):
    return {person_id: 'It exists!'}

''' Validations request body and validations models '''
@app.put(path='/persons/{person_id}', status_code=status.HTTP_200_OK)
def update_person(
    person_id: int = Path(
        default=...,
        ge=1,
        title='Person ID',
        description='Person ID (1), It is required!',
        example=1,
    ),
    person: Person = Body(default=...),
    location: Location = Body(default=...),
):
    # return person.dict() & location.dict()
    results = person.dict()
    results.update(location.dict())
    return results

''' Form Data parameters '''
@app.post(
    path='/login',
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
)
def login(
    username: str = Form(
        default=...,
        min_length=1,
        max_length=20,
        title='Username',
        description='Username (mappedev)',
        example='mappedev',
    ),
    password: str = Form(
        default=...,
        min_length=8,
        title='Password',
        description='Password (12345678)',
        example='12345678',
    )
):
    return LoginOut(username=username)

''' Cookies and Headers parameters'''
@app.post(path='/contact', status_code=status.HTTP_200_OK)
def contact(
    first_name: str = Form(
        default=...,
        max_length=20,
        min_length=1,
        title='First name',
        description='First name (Mario)',
        example='Mario',
    ),
    last_name: str = Form(
        default=...,
        max_length=20,
        min_length=1,
        title='Last name',
        description='Last name (Peña)',
        example='Peña',
    ),
    email: EmailStr = Form(default=...),
    message: str = Form(default=..., min_length=20),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None),
):
    return user_agent
