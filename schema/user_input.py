from pydantic import BaseModel,Field,computed_field,field_validator
from typing import Literal,Annotated
from config.city_tier import teir_1_cities,tier_2_cities
# pydantic model to validate incoming data
class UserInput(BaseModel):

    # sehema 
    age: Annotated[int,Field(...,description='User Age(years)',examples=[23,45],gt=0,lt=120)]
    weight: Annotated[float,Field(...,description='User weight(kg)',examples=[23])]
    height:  Annotated[float,Field(...,description='User Height(m)',examples=[1.7])]
    income_lpa : Annotated[float,Field(...,description='User annual income(lpa)',gt=0)]
    smoker : Annotated[bool,Field(...,description='is user a smoker ',examples=['True','False'])]
    city: Annotated[str,Field(...,description='user city',examples=['New Delhi','Mumbai'])]
    occupation: Annotated[Literal['retired','freelancer','student','government_job',
 'business_owner','unemployed','private_job'],
 Field(...,description='user occupation',examples=['private_job'])]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2),2)
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'High'
        elif self.smoker and self.bmi > 27:
            return 'median'
        return 'low'
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'Young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle_aged'
        return 'senior'
    @computed_field
    @property
    def city_tier(self) -> int: 
       
        if self.city in teir_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        return 3
    @field_validator('city')
    @classmethod
    def normalize_city(cls,v:str)->str:
        v = v.strip().title()
        return v