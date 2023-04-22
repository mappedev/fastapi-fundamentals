''' Python imports '''
from enum import Enum

''' Pydantic imports '''
from pydantic import BaseModel, EmailStr, Field, HttpUrl, PaymentCardNumber

''' FastAPI imports '''
from fastapi import (
    Body, Cookie, FastAPI,
    File, Form, Header,
    HTTPException, Query, Path,
    status, UploadFile,
)

app = FastAPI()


''' Models '''
class Tags(Enum):
    home = 'Home'
    persons = 'Persons'
    contacts = 'Contacts'
    files = 'Files'


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
    is_married: bool | None = Field(
        default=False,
        example=False,
    )
    ''' Exotic types '''
    email: EmailStr = Field(
        default=...,
        example='user@email.com',
    )
    hair_color: HairColor | None = Field(
        default=None,
        example='black',
    )
    website_url: HttpUrl | None = Field(
        default=None,
        example='https://mappedev.com',
    )
    credit_card: PaymentCardNumber | None = Field(
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


class PersonLocationOut(PersonOut, Location):
    pass


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


@app.get(
    path='/',
    status_code=status.HTTP_200_OK,
    tags=[Tags.home],
    summary='Home',
)
def home() -> dict[str, str]:
    '''
    ## Home endpoint
    '''
    return {'Hello': 'World'}

''' Request and response body '''
@app.post(
    path='/persons',
    # response_model=PersonOut, # Si el path operation function tiene un return hint, no hace falta
    # response_model=Person,
    # response_model_exclude={'password'}
    # Puedes usar las dos anteriores, pero en la documentación te indicará que devolverá la contraseña por el response_model de Person
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.persons], # Permite agrupar el endpoint en tags en la documentación
    summary='Create Person in the app', # Título personalizado para el path operation function
)
def create_person(person: Person = Body(...)) -> PersonOut: # Si el path operation decorator tiene un response_model, o hace falta indicar el return hint
    # Docstring:
    # Title
    # Description
    # Parameters
    # Result
    '''
    ## Create Person

    This path operation creates a person in the app and save the information in the database.

    Parameters:
    - Request body parameters
        - **person: Person** -> A person model with first name, last name, age, email and password as a minimum.
    
    Returns a person out model with first name, last name, age, and email, marital status, hair color, website url and credit card.
    '''
    return person

''' Validations query parameters '''
@app.get(
    path='/persons',
    status_code=status.HTTP_200_OK,
    tags=[Tags.persons],
    summary='Get persons in the app',
    # description='HI FIVE!', # No lo coloque si tienes un DocString que describa el path operation function
    deprecated=True,
)
def get_persons(
    name: str | None = Query(
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
) -> dict[str, int]:
    '''
    ## Get persons

    This path operation gets multiples persons in the app.

    Parameters:
    - Query parameters
        - **age: int** -> Greather and equal than 0.
        - name: str -> [1..50] characters and by default is Anonymous.
    
    Returns a JSON with the name as a key and the age as a value.
    '''
    return {name: age}

persons = [1, 2, 3, 4, 5]

''' Validations path parameters'''
@app.get(
    path='/persons/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=[Tags.persons],
    summary='Get a person in the app',
)
def get_person(
    person_id: int = Path(
        default=...,
        ge=1,
        title='Person ID',
        description='Person ID (1), It is required!',
        example=1,
    ),
) -> dict[str, int]:
    '''
    ## Get a person

    This path operation gets a person in the app.

    Parameters:
    - Path parameters
        - **person_id: int** -> Greather and equal than 1.
    
    Returns a JSON with the person_id as a key and "It exists!" as a value if the person exists in the database.
    '''
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='This person does not exist'
        )
    return {person_id: 'It exists!'}

''' Validations request body and validations models '''
@app.put(
    path='/persons/{person_id}',
    status_code=status.HTTP_200_OK,
    tags=[Tags.persons],
    summary='Update a person in the app',
)
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
) -> PersonLocationOut:
    '''
    ## Update a person

    This path operation updates a person in the app.

    Parameters:
    - Request body parameters
        - **person: Person** -> A person model with first name, last name, age, email and password as a minimum.
        - **location: Location** -> A location model with country, city and state.
    - Path parameters
        - **person_id: int** -> Greather and equal than 1.
    
    Returns a JSON with the person location out model.
    '''
    # return person.dict() & location.dict()
    # results = PersonOut(**person.dict()).dict()
    results = person.dict()
    results.update(location.dict())
    return results

''' Form Data parameters '''
@app.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    tags=[Tags.persons],
    summary='Login a person in the app',
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
) -> LoginOut:
    '''
    ## Login a person

    This path operation logins a person in the app.

    Parameters:
    - Request form parameters
        - **username: str** -> [1..20] A username to login.
        - **password: str** -> [8..255] A password to login.
    
    Returns a JSON with the login out model.
    '''
    return LoginOut(username=username)

''' Cookies and Headers parameters'''
@app.post(
    path='/contact',
    status_code=status.HTTP_200_OK,
    tags=[Tags.contacts],
    summary='Contact the company',
)
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
    user_agent: str | None = Header(default=None),
    ads: str | None = Cookie(default=None),
) -> str | None:
    '''
    ## Contact with the company

    This path operation contracts a person with the company.

    Parameters:
    - Request form parameters
        - **first_name: str** -> [1..20] A first_name to contact.
        - **last_name: str** -> [1..20] A last name to contact.
        - **email: EmailStr** -> A email to contact.
        - **message: str** -> [20..255] A message to contact.
    - Request header parameters
        - user_agent: str -> To watch the user information.
    - Request cookie parameters
        - ads: str -> To watch the user information.
    
    Returns the user agent.
    '''
    return user_agent

@app.post(
    path='/post-image',
    status_code=status.HTTP_200_OK,
    tags=[Tags.files],
    summary='Post a image in the app',
)
def post_image(image: UploadFile = File(
    default=...,
    title='Image file',
    description='Image file',
)) -> dict[str, int]:
    '''
    ## Post a image

    This path operation contracts a person with the company.

    Parameters:
    - Request form parameters
        - **first_name: str** -> [1..20] A first_name to contact.
        - **last_name: str** -> [1..20] A last name to contact.
        - **email: EmailStr** -> A email to contact.
        - **message: str** -> [20..255] A message to contact.
    - Request header parameters
        - user_agent: str -> To watch the user information.
    - Request cookie parameters
        - ads: str -> To watch the user information.
    
    Returns the user agent.
    '''
    return {
        'filename': image.filename,
        'format': image.content_type,
        'size(kb)': round(number=image.size/1024, ndigits=2),
    }