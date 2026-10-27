from pydantic import BaseModel
class EmployeeInput(BaseModel):
    name:str
    role:str
    email:str