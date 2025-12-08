import click
from flask.cli import with_appcontext
from datetime import date
from .salary import pay_salaries
from .models import (
    db,
    Division,
    Department,
    Building,
    Project,
    Employee,
    EmployeeProject,
    Room,
    EmployeeRoom,
    DepartmentRoom,
    EmployeeTitle,
    SalaryPayment,
)

@click.command('seed-db')
@with_appcontext
def seed_db():
    
    Department.query.update({Department.employee_no: None})
    Division.query.update({Division.employee_no: None})
    Project.query.update({Project.manager_id: None})
    db.session.commit()

    SalaryPayment.query.delete()
    EmployeeProject.query.delete()
    EmployeeRoom.query.delete()
    DepartmentRoom.query.delete()
    EmployeeTitle.query.delete()
    Employee.query.delete()        
    Project.query.delete()        
    Room.query.delete()
    Department.query.delete()   
    Building.query.delete()
    Division.query.delete()
    
    
    db.session.commit()

    # Divisions
    tech = Division(division_name="Technology", employee_no=None)
    ops = Division(division_name="Operations", employee_no=None)
    db.session.add_all([tech, ops])
    db.session.commit()

    # Departments
    se = Department(department_name="Software Engineering", budget=300000, division_name="Technology", employee_no=None)
    net = Department(department_name="Network Operations", budget=180000, division_name="Operations", employee_no=None)
    hr = Department(department_name="Human Resources", budget=130000, division_name="Operations", employee_no=None)
    db.session.add_all([se, net, hr])
    db.session.commit()

    # Buildings
    b1 = Building(building_code="A1", name="Main Campus", year_bought=2012, cost=2400000)
    b2 = Building(building_code="B2", name="Research Annex", year_bought=2018, cost=1400000)
    db.session.add_all([b1, b2])
    db.session.commit()

    # Rooms
    r101 = Room(office_number="101A", square_feet=225, type="Office", building_code="A1")
    r102 = Room(office_number="102A", square_feet=320, type="Conference", building_code="A1")
    r203 = Room(office_number="203B", square_feet=180, type="Office", building_code="B2")
    db.session.add_all([r101, r102, r203])
    db.session.commit()

    # DepartmentRooms
    db.session.add_all([
        DepartmentRoom(department_name="Software Engineering", office_number="101A"),
        DepartmentRoom(department_name="Network Operations", office_number="203B"),
        DepartmentRoom(department_name="Human Resources", office_number="102A")
    ])
    db.session.commit()

    # Employees
    e1 = Employee(employee_no=1, employee_name="Alice Johnson", phone_number="555-1001", title="Senior Developer", department_name="Software Engineering")
    e2 = Employee(employee_no=2, employee_name="Bob Smith", phone_number="555-2002", title="Network Specialist", department_name="Network Operations")
    e3 = Employee(employee_no=3, employee_name="Sarah Lee", phone_number="555-3003", title="HR Manager", department_name="Human Resources")
    e4 = Employee(employee_no=4, employee_name="Michael Chen", phone_number="555-4004", title="Division Analyst", department_name=None)
    db.session.add_all([e1, e2, e3, e4])
    db.session.commit()

    # Assign heads
    tech.employee_no = 4      # Michael Chen is Technology division head
    se.employee_no = 1        # Alice Johnson is Software Engineering dept head
    net.employee_no = 2       # Bob Smith is Network Operations dept head
    hr.employee_no = 3        # Sarah Lee is HR dept head
    db.session.commit()

    # EmployeeRooms (office assignments)
    db.session.add_all([
        EmployeeRoom(employee_no=1, office_number="101A"),
        EmployeeRoom(employee_no=4, office_number="101A"),  # Shared office
        EmployeeRoom(employee_no=2, office_number="203B"),
        EmployeeRoom(employee_no=3, office_number="102A"),
    ])
    db.session.commit()

    # Projects
    p1 = Project(project_number=501, budget=120000, date_started=date(2024, 1, 10), date_ended=None, manager_id=1)
    p2 = Project(project_number=502, budget=80000, date_started=date(2023, 5, 20), date_ended=date(2024, 2, 20), manager_id=2)
    db.session.add_all([p1, p2])
    db.session.commit()

    # EmployeeProject assignments (history)
    db.session.add_all([
        EmployeeProject(employee_no=1, project_number=501, hours_worked=300, role="Lead Developer"),
        EmployeeProject(employee_no=2, project_number=502, hours_worked=450, role="Network Lead"),
        EmployeeProject(employee_no=4, project_number=501, hours_worked=120, role="Data Analyst"),
    ])
    db.session.commit()

    # EmployeeTitles (example titles and salaries)
    db.session.add_all([
        EmployeeTitle(title="Junior Developer", salary=60000),
        EmployeeTitle(title="Senior Developer", salary=90000),
        EmployeeTitle(title="Network Specialist", salary=75000),
        EmployeeTitle(title="HR Manager", salary=80000),
        EmployeeTitle(title="Division Analyst", salary=70000),
    ])
    db.session.commit()

    salaries = [
        # employee_no, gross_salary, payment_date
        (1, 90000, date(2025, 11, 30)),
        (2, 75000, date(2025, 11, 30)),
        (3, 80000, date(2025, 11, 30)),
        (4, 70000, date(2025, 11, 30)),
    ]

    for emp_no, gross, pay_date in salaries:
        federal_tax = gross * 0.10
        state_tax = gross * 0.05
        other_tax = gross * 0.03
        net = gross - (federal_tax + state_tax + other_tax)
        payment = SalaryPayment(
            employee_no=emp_no,
            payment_date=pay_date,
            gross_salary=gross,
            federal_tax=federal_tax,
            state_tax=state_tax,
            other_tax=other_tax,
            net_salary=net
        )
        db.session.add(payment)

    db.session.commit()

    db.session.commit()
    click.echo("Database cleared and seeded with fresh sample data successfully!")

@click.command('pay-salaries')
@with_appcontext
def pay_salaries_command():
    today = date.today()
    pay_salaries(today)
    click.echo(f"Salaries paid for {today.strftime('%B %Y')}")

def register_commands(app):
    app.cli.add_command(seed_db)
    app.cli.add_command(pay_salaries_command)