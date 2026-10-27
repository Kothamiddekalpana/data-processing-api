from fastapi import FastAPI
from employee import Employee
from EmployeeInput import EmployeeInput 
import json
from pathlib import Path

app = FastAPI()
emp = Employee()
employees = []
DATA_FILE = Path(__file__).parent / "employees.json"

@app.get("/")
def home():
    return {"message": "Data Processing API is running!"}

@app.get("/myOwnTest")
def myOwnTest():
    return {"message":"You are doing great jon Ms.Kalpana"}

@app.get("/employees")
def get_employee():
    employees = load_employees()
    return employees

@app.get("/employees/{emp_id}")
def get_employee_by_id(emp_id:int):
    employees = load_employees()
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    return {"message" : "No Employee Found With This Id"}



@app.post("/addEmployee")
def add_employee(employee:EmployeeInput):
    employees = load_employees()
    new_id = max((emp["id"] for emp in employees),default = 0)+1
    new_emp = {
        "id":new_id,
        **employee.model_dump()
    }
    employees.append(new_emp)
    with open(DATA_FILE,"w") as file:
        json.dump(employees,file,indent=4)
    return {"message" : "Successfully Added"}

def load_employees():
    with open(DATA_FILE,"r") as file:
        return json.load(file)

@app.put("/update_employee/{emp_id}")    
def update_employee(emp_id:int,update_employee:EmployeeInput):
    employees = load_employees()
    for emp in employees:
        if emp["id"] == emp_id:
            emp["name"] = update_employee.name
            emp["role"] = update_employee.role
            with open(DATA_FILE,"w") as file:
                json.dump(employees,file,indent=4)

            return {"message" :"Succesfully Updated"}
    return {"message" : "Employee not found with the Id"}

@app.delete("/delete_employee/{emp_id}")
def delete_employee(emp_id:int):
    employees = load_employees()
    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            with open(DATA_FILE,"w") as file:
                json.dump(employees,file,indent=4)
                return {"message":"Successfully removed Employee",
                        "employee" :emp}
    return {"message" : "No Employee Found With Id"}