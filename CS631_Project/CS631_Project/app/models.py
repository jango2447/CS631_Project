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



class Employee(db.Model):
    __tablename__ = 'employees'
    employee_no = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    title = db.Column(db.String(50))
    department_name = db.Column(
        db.String(50),
        db.ForeignKey('departments.department_name', name='fk_employees_department_name')
    )
    is_active = db.Column(db.Boolean, default=True)
    employment_start_date = db.Column(db.Date, nullable=True, default=date.today)
    employment_end_date = db.Column(db.Date, nullable=True)
    managed_projects = db.relationship("Project", back_populates="manager")
    projects = db.relationship("ProjectTeam", back_populates="employee")
    def __repr__(self):
        return f"<Employee {self.name}>"

class ProjectTeam(db.Model):
    __tablename__ = "project_team"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_number", ondelete="CASCADE"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_no", ondelete="CASCADE"))

    project = db.relationship("Project", back_populates="team")
    employee = db.relationship("Employee", back_populates="projects")

    __table_args__ = (
        db.UniqueConstraint("project_id", "employee_id", name="uq_project_employee"),
    )

class Milestone(db.Model):
    __tablename__ = "milestones"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_number", ondelete="CASCADE"))
    project = db.relationship("Project", back_populates="milestones")

    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    status = db.Column(db.String(20)) 
    due_date = db.Column(db.Date)

    def __repr__(self):
        return f"<Milestone {self.title}>"

class WorkLog(db.Model):
    __tablename__ = "work_logs"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_number", ondelete="CASCADE"))
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.employee_no", ondelete="CASCADE"))

    project = db.relationship("Project", back_populates="worklogs")
    employee = db.relationship("Employee")

    hours_worked = db.Column(db.Numeric(6, 2), nullable=False)
    work_date = db.Column(db.Date, server_default=db.func.current_date())

    def __repr__(self):
        return f"<WorkLog {self.hours_worked}h>"

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

class EmployeeSalary(db.Model):
    __tablename__ = 'employee_salaries'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_no = db.Column(db.Integer, db.ForeignKey('employees.employee_no'), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # Null means current salary
    type = db.Column(db.String(20), nullable=False)  # 'salary' or 'hourly'

    employee = db.relationship('Employee', backref=db.backref('salaries', lazy=True))

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

class Project(db.Model):
    __tablename__ = 'projects'
    name = db.Column(db.String(150))
    description = db.Column(db.Text)
    project_number = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    manager_id = db.Column(db.Integer, db.ForeignKey('employees.employee_no'))
    manager = db.relationship("Employee", back_populates="managed_projects")
    worklogs = db.relationship("WorkLog", back_populates="project", cascade="all, delete-orphan")
   
    team = db.relationship(
        "ProjectTeam",
        back_populates="project",
        cascade="all, delete"
    )

    milestones = db.relationship(
        "Milestone",
        back_populates="project",
        cascade="all, delete"
    )
    @property
    def milestones_json(self):
       return [
           {
               "title": m.title,
               "description": m.description,
               "status": m.status,
               "due_date": m.due_date.strftime("%Y-%m-%d") if m.due_date else ""
           }
           for m in self.milestones
       ]
    def __repr__(self):
        return f"<Project {self.name}>"


