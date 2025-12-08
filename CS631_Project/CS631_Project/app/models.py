from . import db
from datetime import datetime
from datetime import date

class Division(db.Model):
    __tablename__ = 'divisions'
    division_name = db.Column(db.String(50), primary_key=True)
    employee_no = db.Column(db.Integer, db.ForeignKey('employees.employee_no', name='fk_divisions_employee_no'))  # division head

class Department(db.Model):
    __tablename__ = 'departments'
    department_name = db.Column(db.String(50), primary_key=True)
    budget = db.Column(db.Float)
    division_name = db.Column(db.String(50), db.ForeignKey('divisions.division_name', name='fk_departments_division_name'))
    employee_no = db.Column(db.Integer, db.ForeignKey('employees.employee_no', name='fk_departments_employee_no'))  # department head


class Building(db.Model):
    __tablename__ = 'buildings'
    building_code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100))
    year_bought = db.Column(db.Integer)
    cost = db.Column(db.Float)

class Project(db.Model):
    __tablename__ = 'projects'
    project_number = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Float)
    date_started = db.Column(db.Date)
    date_ended = db.Column(db.Date)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.employee_no'))

class Employee(db.Model):
    __tablename__ = 'employees'
    employee_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    title = db.Column(db.String(50))
    department_name = db.Column(db.String(50), db.ForeignKey('departments.department_name', name='fk_employees_department_name'))

class EmployeeProject(db.Model):
    __tablename__ = 'employee_projects'
    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.Integer, db.ForeignKey('employees.employee_no'))
    project_number = db.Column(db.Integer, db.ForeignKey('projects.project_number'))
    hours_worked = db.Column(db.Float)
    role = db.Column(db.String(50))

class Room(db.Model):
    __tablename__ = 'rooms'
    office_number = db.Column(db.String(10), primary_key=True)
    square_feet = db.Column(db.Float)
    type = db.Column(db.String(20))
    building_code = db.Column(db.String(10), db.ForeignKey('buildings.building_code'))

class EmployeeRoom(db.Model):
    __tablename__ = 'employee_rooms'
    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.Integer, db.ForeignKey('employees.employee_no'))
    office_number = db.Column(db.String(10), db.ForeignKey('rooms.office_number'))

class DepartmentRoom(db.Model):
    __tablename__ = 'department_rooms'
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(50), db.ForeignKey('departments.department_name'))
    office_number = db.Column(db.String(10), db.ForeignKey('rooms.office_number'))

class EmployeeTitle(db.Model):
    __tablename__ = 'employee_titles'
    title = db.Column(db.String(50), primary_key=True)
    salary = db.Column(db.Float)

class SalaryPayment(db.Model):
    __tablename__ = 'salary_payments'

    id = db.Column(db.Integer, primary_key=True)
    employee_no = db.Column(db.Integer, db.ForeignKey('employees.employee_no'), nullable=False)
    payment_date = db.Column(db.Date, default=date.today, nullable=False)
    gross_salary = db.Column(db.Float, nullable=False)
    federal_tax = db.Column(db.Float, nullable=False)
    state_tax = db.Column(db.Float, nullable=False)
    other_tax = db.Column(db.Float, nullable=False)
    net_salary = db.Column(db.Float, nullable=False)

    # Relationship for easy access to employee from salary payment
    employee = db.relationship('Employee', backref=db.backref('salary_payments', lazy=True))
