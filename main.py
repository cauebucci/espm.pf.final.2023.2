from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
import datetime

app = FastAPI()

engine = create_engine('mysql+pymysql://root:SenhaRoot@localhost:3306/Jobs')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class Job(Base):
    __tablename__ = 'Job'

    JobId = Column(Integer, primary_key=True)
    Name = Column(String(255))
    Description = Column(String(255))
    Employee = relationship('Employee')


class Employee(Base):
    __tablename__ = 'Employee'

    EmployeeId = Column(Integer, primary_key=True)
    JobId = Column(
        Integer, ForeignKey('Job.JobId', ondelete='CASCADE')) 
    Name = Column(String(255))
    Birthday = Column(DateTime) 
    Salary = Column(Float)
    Departmemt = Column(String(255))
    Job = relationship('Job')
    JobHistory = relationship('JobHistory')


class JobHistory(Base):
    __tablename__ = 'JobHistory'

    JobHistoryId = Column(Integer, primary_key=True)
    EmployeeID = Column(
        Integer, ForeignKey('Employee.EmployeeId', ondelete='CASCADE')) 
    Title = Column(String(255))
    StartDate = Column(DateTime) 
    EndDate = Column(DateTime)
    Salary = Column(Float)
    Job = Column(String(255))
    Employee = relationship('Employee')


Base.metadata.create_all(bind=engine)


@app.post("/jobs")
def create_job(name: str, description: str):
    job = Job(Name=name, Description=description)
    session.add(job)
    session.commit()

    return JSONResponse(content={'JobId': job.JobId, 'name': job.Name})

@app.put("/jobs")
def put_job(id: str, name: str, description: str):
    job = session.query(Job).filter_by(JobId=id).first()
    job.Name = name
    job.Description = description
    session.commit()

    return JSONResponse(content={'JobId': job.JobId, 'name': job.Name, 'description': job.Description})

@app.get("/jobs/{job_id}")
def get_job(job_id: int):
    job = session.query(Job).filter(Job.JobId == job_id).first()
    
    return JSONResponse(content={'JobId': job.JobId, 'name': job.Name, 'description': job.Description})

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    job = session.query(Job).filter(Job.JobId == job_id).first()
    session.delete(job)
    session.commit()
    
    return JSONResponse(content={'JobId': job.JobId, 'name': job.Name, 'description': job.Description})


@app.get("/jobs")
def read_jobs():
    jobs = session.query(Job).all()

    job_list = []

    for job in jobs:
        job_dict = {'JobId': job.JobId, 'name': job.Name, 'description': job.Description}
        job_list.append(job_dict)

    return JSONResponse(content=job_list)



@app.post("/employees")
def create_employees(job_id: int, name: str, birthday: str, salary: float, department: str):
    employee = Employee(JobId=job_id, Name=name, Birthday=birthday, Salary=salary, Departmemt=department)
    session.add(employee)
    session.commit()

    return JSONResponse(content={'EmployeeId': employee.EmployeeId, 'JobId': employee.JobId, 'name': employee.Name, 'birthday': str(employee.Birthday), 'salary': employee.Salary, 'department': employee.Departmemt})

@app.put("/employees")
def put_employees(employee_id: int, job_id: int, name: str, birthday: str, salary: float, department: str):
    employees = session.query(Employee).filter_by(EmployeeId=employee_id).first()
    employees.JobID = job_id
    employees.Name = name
    employees.Birthday = birthday
    employees.Salary = salary
    employees.Department = department
    session.commit()

    return JSONResponse(content={'EmployeeId': employees.EmployeeId, 'JobId': employees.JobId, 'name': employees.Name, 'salary': employees.Salary, 'department': employees.Departmemt})

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    employee = session.query(Employee).filter(Employee.EmployeeId == employee_id).first()
    
    return JSONResponse(content={'EmployeeId': employee.EmployeeId, 'JobId': employee.JobId, 'name': employee.Name, 'birthday': str(employee.Birthday), 'salary': employee.Salary, 'department': employee.Departmemt})

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    employee = session.query(Employee).filter(Employee.EmployeeId == employee_id).first()
    session.delete(employee)
    session.commit()
    return JSONResponse(content={'EmployeeId': employee.EmployeeId, 'JobId': employee.JobId, 'name': employee.Name, 'birthday': str(employee.Birthday), 'salary': employee.Salary, 'department': employee.Departmemt})


@app.get("/employees")
def read_employees():
    query = session.query(Job).join(Employee).all()

    list = []
    for item in query:
        for employee in item.Employee:
            employees = {'EmployeeId': employee.EmployeeId, 'JobId': employee.JobId, 'name': employee.Name, 'Birthday': str(employee.Birthday),  'salary': employee.Salary, 'department': employee.Departmemt}
            dict = {'JobId': item.JobId, 'name': item.Name, 'description': item.Description, 'Employees': employees}
            list.append(dict)

    return JSONResponse(content=list)

@app.post("/JobHistorys")
def create_jobhistory(employee_id: int, title: str, startdate: str, enddate: str, salary: float, job: str):
    jobhistory = JobHistory(EmployeeID=employee_id, Title=title, StartDate=startdate, EndDate=enddate, Salary=salary, Job=job)
    session.add(jobhistory)
    session.commit()

    return JSONResponse(content={'JobHistoryId': jobhistory.JobHistoryId, 'Title': jobhistory.Title, 'startdate': str(jobhistory.StartDate), 'enddate': str(jobhistory.EndDate), 'salary': jobhistory.Salary, 'Job': jobhistory.Job})


@app.put("/JobHistorys")
def put_jobhistory(jobhistory_id: int, employee_id: int, title: str, startdate: str, enddate: str, salary: float, job: str):
    jobhistory = session.query(JobHistory).filter_by(JobHistoryId=jobhistory_id).first()
    jobhistory.EmployeeId = employee_id
    jobhistory.title = title
    jobhistory.StartDate = startdate
    jobhistory.EndDate = enddate
    jobhistory.Salary = salary
    jobhistory.Job = job
    session.commit()

    return JSONResponse(content={'JobHistoryId': jobhistory.JobHistoryId, 'Title': jobhistory.Title, 'startdate': str(jobhistory.StartDate), 'enddate': str(jobhistory.EndDate), 'salary': jobhistory.Salary, 'Job': jobhistory.Job})

@app.get("/JobHistorys/{jobhistory_id}")
def read_jobhistory(jobhistory_id: int):
    jobhistory = session.query(JobHistory).filter(JobHistory.JobHistoryId == jobhistory_id).first()
    
    return JSONResponse(content={'JobHistoryId': jobhistory.JobHistoryId, 'Title': jobhistory.Title, 'startdate': str(jobhistory.StartDate), 'enddate': str(jobhistory.EndDate), 'salary': jobhistory.Salary, 'Job': jobhistory.Job})

@app.delete("/JobHistorys/{jobhistory_id}")
def delete_jobhistory(jobhistory_id: int):
    jobhistory = session.query(JobHistory).filter(JobHistory.JobHistoryId == jobhistory_id).first()
    session.delete(jobhistory)
    session.commit()

    return JSONResponse(content={'JobHistoryId': jobhistory.JobHistoryId, 'Title': jobhistory.Title, 'startdate': str(jobhistory.StartDate), 'enddate': str(jobhistory.EndDate), 'salary': jobhistory.Salary, 'Job': jobhistory.Job})


@app.get("/JobHistorys")
def read_jobhistory():
    query = session.query(Employee).join(JobHistory).all()

    list = []

    for item in query:
        for jobhistory in item.JobHistory:
            jobhistorys = {'JobHistoryId': jobhistory.JobHistoryId, 'Title': jobhistory.Title, 'startdate': str(jobhistory.StartDate), 'enddate': str(jobhistory.EndDate), 'salary': jobhistory.Salary, 'Job': jobhistory.Job}
            dict = {'EmployeeId': item.EmployeeId, 'JobId': item.JobId, 'name': item.Name, 'birthday': str(item.Birthday), 'salary': item.Salary, 'department': item.Departmemt, 'JobHistorys' : jobhistorys}
            list.append(dict)

    return JSONResponse(content=list)