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
    me = Department(department_name="Mechanical Engineering", budget=130000, division_name="Technology", employee_no=None)
    db.session.add_all([se, net, hr,me])
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
    e1 = Employee(
        employee_no=1,
        employee_name="Alice Johnson",
        phone_number="555-1001",
        title="Head of Technology",
        department_name=None,
        employment_start_date=date(2021, 2, 15)
    )

    e2 = Employee(
        employee_no=2,
        employee_name="Bob Smith",
        phone_number="555-2002",
        title="Head of Operations",
        department_name=None,
        employment_start_date=date(2020, 7, 1)
    )

    e3 = Employee(
        employee_no=3,
        employee_name="Sarah Lee",
        phone_number="555-3003",
        title="Head of Human Resources",
        department_name="Human Resources",
        employment_start_date=date(2019, 11, 12)
    )

    e4 = Employee(
        employee_no=4,
        employee_name="Michael Chen",
        phone_number="555-4004",
        title="Project Manager",
        department_name="Human Resources",
        employment_start_date=date(2022, 4, 21)
    )

    e5 = Employee(
        employee_no=5,
        employee_name="Emma Davis",
        phone_number="555-5005",
        title="Project Manager",
        department_name="Human Resources",
        employment_start_date=date(2018, 5, 20)
    )

    e6 = Employee(
        employee_no=6,
        employee_name="James Wilson",
        phone_number="555-6006",
        title="Recruitment Specialist",
        department_name="Human Resources",
        employment_start_date=date(2021, 8, 10)
    )

    e7 = Employee(
        employee_no=7,
        employee_name="Olivia Martinez",
        phone_number="555-7007",
        title="HR Training Coordinator",
        department_name="Human Resources",
        employment_start_date=date(2019, 3, 8)
    )

    e8 = Employee(
        employee_no=8,
        employee_name="Liam Brown",
        phone_number="555-8008",
        title="Compensation Analyst",
        department_name="Human Resources",
        employment_start_date=date(2020, 1, 25)
    )

    e9 = Employee(
        employee_no=9,
        employee_name="Sophia Anderson",
        phone_number="555-9009",
        title="Employee Relations Specialist",
        department_name="Human Resources",
        employment_start_date=date(2017, 12, 11)
    )

    e10 = Employee(
        employee_no=10,
        employee_name="Noah Thomas",
        phone_number="555-1010",
        title="Head of Mechanical Engineering",
        department_name="Mechanical Engineering",
        employment_start_date=date(2016, 6, 30)
    )

    e11 = Employee(
        employee_no=11,
        employee_name="Isabella Taylor",
        phone_number="555-1111",
        title="Project Manager",
        department_name="Mechanical Engineering",
        employment_start_date=date(2019, 9, 15)
    )

    e12 = Employee(
        employee_no=12,
        employee_name="Mason Moore",
        phone_number="555-1212",
        title="Project Manager",
        department_name="Mechanical Engineering",
        employment_start_date=date(2015, 4, 2)
    )

    e13 = Employee(
        employee_no=13,
        employee_name="Mia Jackson",
        phone_number="555-1313",
        title="Mechanical Design Engineer",
        department_name="Mechanical Engineering",
        employment_start_date=date(2022, 7, 19)
    )

    e14 = Employee(
        employee_no=14,
        employee_name="Ethan White",
        phone_number="555-1414",
        title="Manufacturing Engineer",
        department_name="Mechanical Engineering",
        employment_start_date=date(2018, 10, 5)
    )

    e15 = Employee(
        employee_no=15,
        employee_name="Amelia Harris",
        phone_number="555-1515",
        title="Quality Control Engineer",
        department_name="Mechanical Engineering",
        employment_start_date=date(2020, 11, 3)
    )

    e16 = Employee(
        employee_no=16,
        employee_name="Alexander Martin",
        phone_number="555-1616",
        title="Maintenance Engineer",
        department_name="Mechanical Engineering",
        employment_start_date=date(2017, 2, 17)
    )

    e17 = Employee(
        employee_no=17,
        employee_name="Charlotte Garcia",
        phone_number="555-1717",
        title="Head of Network Operations",
        department_name="Network Operations",
        employment_start_date=date(2021, 5, 27)
    )

    e18 = Employee(
        employee_no=18,
        employee_name="Daniel Martinez",
        phone_number="555-1818",
        title="Project Manager",
        department_name="Network Operations",
        employment_start_date=date(2019, 8, 13)
    )

    e19 = Employee(
        employee_no=19,
        employee_name="Emily Rodriguez",
        phone_number="555-1919",
        title="Project Manager",
        department_name="Network Operations",
        employment_start_date=date(2018, 1, 23)
    )

    e20 = Employee(
        employee_no=20,
        employee_name="Matthew Lewis",
        phone_number="555-2020",
        title="Network Security Specialist",
        department_name="Network Operations",
        employment_start_date=date(2022, 3, 29)
    )

    e21 = Employee(
        employee_no=21,
        employee_name="Abigail Walker",
        phone_number="555-2121",
        title="Network Technician",
        department_name="Network Operations",
        employment_start_date=date(2020, 9, 10)
    )

    e22 = Employee(
        employee_no=22,
        employee_name="David Hall",
        phone_number="555-2222",
        title="Systems Analyst",
        department_name="Network Operations",
        employment_start_date=date(2016, 12, 1)
    )

    e23 = Employee(
        employee_no=23,
        employee_name="Elizabeth Allen",
        phone_number="555-2323",
        title="Telecommunications Specialist",
        department_name="Network Operations",
        employment_start_date=date(2017, 7, 7)
    )

    e24 = Employee(
        employee_no=24,
        employee_name="Joseph Young",
        phone_number="555-2424",
        title="Head of Software Engineering",
        department_name="Software Engineering",
        employment_start_date=date(2019, 10, 16)
    )

    e25 = Employee(
        employee_no=25,
        employee_name="Madison King",
        phone_number="555-2525",
        title="Project Manager",
        department_name="Software Engineering",
        employment_start_date=date(2021, 6, 14)
    )

    e26 = Employee(
        employee_no=26,
        employee_name="Samuel Wright",
        phone_number="555-2626",
        title="Project Manager",
        department_name="Software Engineering",
        employment_start_date=date(2022, 1, 12)
    )

    e27 = Employee(
        employee_no=27,
        employee_name="Ella Scott",
        phone_number="555-2727",
        title="Software Developer",
        department_name="Software Engineering",
        employment_start_date=date(2018, 4, 18)
    )

    e28 = Employee(
        employee_no=28,
        employee_name="Benjamin Green",
        phone_number="555-2828",
        title="QA Engineer",
        department_name="Software Engineering",
        employment_start_date=date(2020, 5, 22)
    )

    e29 = Employee(
        employee_no=29,
        employee_name="Avery Adams",
        phone_number="555-2929",
        title="Technical Architect",
        department_name="Software Engineering",
        employment_start_date=date(2017, 3, 3)
    )

    e30 = Employee(
        employee_no=30,
        employee_name="Jackson Baker",
        phone_number="555-3030",
        title="DevOps Engineer",
        department_name="Software Engineering",
        employment_start_date=date(2019, 11, 29)
    )


    db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10,
                    e11, e12, e13, e14, e15, e16, e17, e18, e19, e20,
                    e21, e22, e23, e24, e25, e26, e27, e28, e29, e30])
    db.session.commit()

    # Assign heads
    tech.employee_no = 1    
    se.employee_no = 24       
    net.employee_no = 17     
    hr.employee_no = 3    
    me.employee_no = 10 
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