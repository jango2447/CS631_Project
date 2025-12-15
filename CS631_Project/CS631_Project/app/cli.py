import click
from flask.cli import with_appcontext
from datetime import date, timedelta
import random
from sqlalchemy import func
from .salary import pay_salaries
from .models import (
    db,
    Division,
    Department,
    Building,
    Project,
    ProjectTeam,
    Employee,
    EmployeeProject,
    Room,
    EmployeeRoom,
    DepartmentRoom,
    EmployeeSalary,
    SalaryPayment,
    WorkLog,
    Milestone
)

@click.command('seed-db')
@with_appcontext
def seed_db():
    
    Department.query.update({Department.employee_no: None})
    Division.query.update({Division.employee_no: None})
    Project.query.update({Project.manager_id: None})
    ProjectTeam.query.update({ProjectTeam.project_id: None})
    ProjectTeam.query.update({ProjectTeam.employee_id: None})
    db.session.commit()


    SalaryPayment.query.delete()
    EmployeeProject.query.delete()
    EmployeeRoom.query.delete()
    DepartmentRoom.query.delete()
    EmployeeSalary.query.delete()
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

    # EmployeeProject assignments (history)
    # db.session.add_all([
    #     EmployeeProject(employee_no=1, project_number=501, hours_worked=300, role="Lead Developer"),
    #     EmployeeProject(employee_no=2, project_number=502, hours_worked=450, role="Network Lead"),
    #     EmployeeProject(employee_no=4, project_number=501, hours_worked=120, role="Data Analyst"),
    # ])
    # db.session.commit()

    # Projects
   
    today = date.today()

    p1 = Project(name="CSC 631 Database", description="Final Project for CSC 631", project_number=501, budget=120000,
                 start_date=today - timedelta(days=180), end_date=today + timedelta(days=30), manager_id=1)

    p2 = Project(name="Website Design", description="Manage and Create your own Website", project_number=502, budget=80000,
                 start_date=today - timedelta(days=400), end_date=today - timedelta(days=10), manager_id=2)

    p3 = Project(name="Mobile App Development", description="Develop a mobile application for campus use", project_number=503, budget=95000,
                 start_date=today + timedelta(days=20), end_date=today + timedelta(days=120), manager_id=1)

    p4 = Project(name="E-Commerce Website", description="Create an online shopping platform", project_number=504, budget=150000,
                 start_date=today - timedelta(days=200), end_date=today + timedelta(days=60), manager_id=2)

    p5 = Project(name="Cloud Migration", description="Migrate systems to cloud infrastructure", project_number=505, budget=200000,
                 start_date=today + timedelta(days=15), end_date=today + timedelta(days=150), manager_id=1)

    p6 = Project(name="Data Analytics Platform", description="Enterprise data analytics solution", project_number=506, budget=175000,
                 start_date=today - timedelta(days=90), end_date=today - timedelta(days=5), manager_id=3)

    p7 = Project(name="AI Recommendation System", description="Machine learning recommendation engine", project_number=507, budget=220000,
                 start_date=today + timedelta(days=50), end_date=today + timedelta(days=180), manager_id=2)

    p8 = Project(name="CRM Implementation", description="Customer relationship management system", project_number=508, budget=85000,
                 start_date=today - timedelta(days=300), end_date=today + timedelta(days=10), manager_id=1)

    p9 = Project(name="Cybersecurity Upgrade", description="Improve enterprise security posture", project_number=509, budget=120000,
                 start_date=today - timedelta(days=60), end_date=today + timedelta(days=120), manager_id=3)

    p10 = Project(name="DevOps Pipeline Automation", description="Automate CI/CD pipelines", project_number=510, budget=110000,
                  start_date=today + timedelta(days=10), end_date=today + timedelta(days=100), manager_id=2)

    p11 = Project(name="ERP System Upgrade", description="Upgrade ERP modules", project_number=511, budget=180000,
                  start_date=today - timedelta(days=500), end_date=today - timedelta(days=50), manager_id=1)

    p12 = Project(name="Blockchain Proof of Concept", description="Blockchain-based transaction prototype", project_number=512, budget=130000,
                  start_date=today + timedelta(days=30), end_date=today + timedelta(days=200), manager_id=3)

    p13 = Project(name="IoT Monitoring System", description="IoT sensors for infrastructure monitoring", project_number=513, budget=140000,
                  start_date=today - timedelta(days=150), end_date=today + timedelta(days=90), manager_id=2)

    p14 = Project(name="UI/UX Redesign", description="Redesign user interface and experience", project_number=514, budget=70000,
                  start_date=today + timedelta(days=5), end_date=today + timedelta(days=60), manager_id=1)

    p15 = Project(name="API Integration Hub", description="Centralized API integration system", project_number=515, budget=125000,
                  start_date=today - timedelta(days=250), end_date=today - timedelta(days=10), manager_id=2)

    p16 = Project(name="Machine Learning Pipeline", description="Automated ML training pipeline", project_number=516, budget=210000,
                  start_date=today + timedelta(days=40), end_date=today + timedelta(days=180), manager_id=3)

    p17 = Project(name="Disaster Recovery Planning", description="Design disaster recovery strategy", project_number=517, budget=90000,
                  start_date=today - timedelta(days=100), end_date=today + timedelta(days=150), manager_id=1)

    p18 = Project(name="Student Information System", description="System for managing student records", project_number=518, budget=135000,
                  start_date=today + timedelta(days=60), end_date=today + timedelta(days=300), manager_id=2)

    p19 = Project(name="Online Learning Platform", description="Web-based learning management system", project_number=519, budget=160000,
                  start_date=today - timedelta(days=50), end_date=today + timedelta(days=80), manager_id=3)

    p20 = Project(name="Library Management System", description="Automate library operations", project_number=520, budget=95000,
                  start_date=today + timedelta(days=20), end_date=today + timedelta(days=150), manager_id=1)

    db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
                        p11, p12, p13, p14, p15, p16, p17, p18, p19, p20])
    db.session.commit()
    #Project Teams

    pt1 = ProjectTeam(project_id=503, employee_id=1)
    pt2 = ProjectTeam(project_id=503, employee_id=2)
    pt3 = ProjectTeam(project_id=503, employee_id=3)


    pt4 = ProjectTeam(project_id=504, employee_id=4)
    pt5 = ProjectTeam(project_id=504, employee_id=5)
    pt6 = ProjectTeam(project_id=504, employee_id=6)


    pt7 = ProjectTeam(project_id=505, employee_id=7)
    pt8 = ProjectTeam(project_id=505, employee_id=8)
    pt9 = ProjectTeam(project_id=505, employee_id=9)


    pt10 = ProjectTeam(project_id=506, employee_id=10)
    pt11 = ProjectTeam(project_id=506, employee_id=11)
    pt12 = ProjectTeam(project_id=506, employee_id=12)


    pt13 = ProjectTeam(project_id=507, employee_id=13)
    pt14 = ProjectTeam(project_id=507, employee_id=14)
    pt15 = ProjectTeam(project_id=507, employee_id=15)


    pt16 = ProjectTeam(project_id=508, employee_id=16)
    pt17 = ProjectTeam(project_id=508, employee_id=17)
    pt18 = ProjectTeam(project_id=508, employee_id=18)


    pt19 = ProjectTeam(project_id=509, employee_id=19)
    pt20 = ProjectTeam(project_id=509, employee_id=20)
    pt21 = ProjectTeam(project_id=509, employee_id=21)


    pt22 = ProjectTeam(project_id=510, employee_id=22)
    pt23 = ProjectTeam(project_id=510, employee_id=23)
    pt24 = ProjectTeam(project_id=510, employee_id=24)


    pt25 = ProjectTeam(project_id=511, employee_id=25)
    pt26 = ProjectTeam(project_id=511, employee_id=26)
    pt27 = ProjectTeam(project_id=511, employee_id=27)


    pt28 = ProjectTeam(project_id=512, employee_id=28)
    pt29 = ProjectTeam(project_id=512, employee_id=29)
    pt30 = ProjectTeam(project_id=512, employee_id=30)


    pt31 = ProjectTeam(project_id=513, employee_id=1)
    pt32 = ProjectTeam(project_id=513, employee_id=4)
    pt33 = ProjectTeam(project_id=513, employee_id=7)


    pt34 = ProjectTeam(project_id=514, employee_id=2)
    pt35 = ProjectTeam(project_id=514, employee_id=5)
    pt36 = ProjectTeam(project_id=514, employee_id=8)


    pt37 = ProjectTeam(project_id=515, employee_id=3)
    pt38 = ProjectTeam(project_id=515, employee_id=6)
    pt39 = ProjectTeam(project_id=515, employee_id=9)


    pt40 = ProjectTeam(project_id=516, employee_id=10)
    pt41 = ProjectTeam(project_id=516, employee_id=13)
    pt42 = ProjectTeam(project_id=516, employee_id=16)


    pt43 = ProjectTeam(project_id=517, employee_id=11)
    pt44 = ProjectTeam(project_id=517, employee_id=14)
    pt45 = ProjectTeam(project_id=517, employee_id=17)


    pt46 = ProjectTeam(project_id=518, employee_id=12)
    pt47 = ProjectTeam(project_id=518, employee_id=15)
    pt48 = ProjectTeam(project_id=518, employee_id=18)


    pt49 = ProjectTeam(project_id=519, employee_id=19)
    pt50 = ProjectTeam(project_id=519, employee_id=22)
    pt51 = ProjectTeam(project_id=519, employee_id=25)


    pt52 = ProjectTeam(project_id=520, employee_id=20)
    pt53 = ProjectTeam(project_id=520, employee_id=23)
    pt54 = ProjectTeam(project_id=520, employee_id=26)
    pt55 = ProjectTeam(project_id=501, employee_id=1)
    pt56 = ProjectTeam(project_id=502, employee_id=2)
    db.session.add_all([
        pt1, pt2, pt3, pt4, pt5, pt6,
        pt7, pt8, pt9, pt10, pt11, pt12,
        pt13, pt14, pt15, pt16, pt17, pt18,
        pt19, pt20, pt21, pt22, pt23, pt24,
        pt25, pt26, pt27, pt28, pt29, pt30,
        pt31, pt32, pt33, pt34, pt35, pt36,
        pt37, pt38, pt39, pt40, pt41, pt42,
        pt43, pt44, pt45, pt46, pt47, pt48,
        pt49, pt50, pt51, pt52, pt53, pt54, pt55, pt56
    ])

    db.session.commit()
    db.session.commit()
    projects = Project.query.all()
    for project in projects:
        if not project.team:
            continue  
        for team_member in project.team:
            employee = team_member.employee
            if not employee:
                continue
            
           
            hours_worked = round(random.uniform(5, 20), 2)
            work_date = date.today() - timedelta(days=random.randint(0, 30))

            worklog = WorkLog(
                project_id=project.project_number,
                employee_id=employee.employee_no,
                hours_worked=hours_worked,
                work_date=work_date
            )

            db.session.add(worklog)


    db.session.commit()
    def create_milestones():
        projects = [
            (501, date(2024, 1, 10)),
            (502, date(2023, 5, 20)),
            (503, date(2024, 2, 1)),
            (504, date(2023, 6, 10)),
            (505, date(2023, 8, 1)),
            (506, date(2024, 1, 15)),
            (507, date(2023, 10, 5)),
            (508, date(2023, 7, 20)),
            (509, date(2024, 3, 1)),
            (510, date(2023, 11, 10)),
            (511, date(2023, 5, 1)),
            (512, date(2024, 2, 20)),
            (513, date(2023, 9, 1)),
            (514, date(2023, 10, 1)),
            (515, date(2024, 1, 25)),
            (516, date(2023, 12, 15)),
            (517, date(2024, 3, 10)),
            (518, date(2023, 8, 15)),
            (519, date(2023, 9, 10)),
            (520, date(2024, 1, 20)),
        ]
       
        milestones = []

        for project_id, start in projects:
            project_obj = Project.query.filter_by(project_number=project_id).first()
            today = date.today()
            milestone_status = "Completed" if project_obj and project_obj.end_date and project_obj.end_date < today else None

            milestones.extend([
                Milestone(
                    project_id=project_id,
                    title="Requirements & Planning",
                    description="Gather requirements, define scope, and create project plan",
                    status=milestone_status or "Pending",
                    due_date=start + timedelta(days=30)
                ),
                Milestone(
                    project_id=project_id,
                    title="Design & Architecture",
                    description="System design, architecture planning, and technology selection",
                    status=milestone_status or "In Progress",
                    due_date=start + timedelta(days=60)
                ),
                Milestone(
                    project_id=project_id,
                    title="Implementation",
                    description="Core development and feature implementation",
                    status=milestone_status or "In Progress",
                    due_date=start + timedelta(days=100)
                ),
                Milestone(
                    project_id=project_id,
                    title="Testing & Deployment",
                    description="System testing, bug fixing, and production deployment",
                    status=milestone_status or "Pending",
                    due_date=start + timedelta(days=120)
                ),
            ])
        db.session.add_all(milestones)
    db.session.commit()
    create_milestones()
    db.session.commit()

    salary_records = [
        # employee_no, salary, start_date, end_date, type

        # 1. Alice Johnson – Head of Technology (salary)
        (1, 85000, date(2021, 2, 15), date(2023, 12, 31), 'salary'),
        (1, 90000, date(2024, 1, 1), None, 'salary'),

        # 2. Bob Smith – Head of Operations (salary)
        (2, 70000, date(2020, 7, 1), date(2024, 5, 31), 'salary'),
        (2, 75000, date(2024, 6, 1), None, 'salary'),

        # 3. Sarah Lee – Head of HR (salary)
        (3, 75000, date(2019, 11, 12), None, 'salary'),

        # 4. Michael Chen – Project Manager (salary)
        (4, 65000, date(2022, 4, 21), date(2023, 12, 31), 'salary'),
        (4, 70000, date(2024, 1, 1), None, 'salary'),

        # 5. Emma Davis – Project Manager (salary)
        (5, 68000, date(2018, 5, 20), None, 'salary'),

        # 6. James Wilson – Recruitment Specialist (hourly)
        (6, 28, date(2021, 8, 10), None, 'hourly'),

        # 7. Olivia Martinez – HR Training Coordinator (hourly)
        (7, 26, date(2019, 3, 8), None, 'hourly'),

        # 8. Liam Brown – Compensation Analyst (salary)
        (8, 64000, date(2020, 1, 25), None, 'salary'),

        # 9. Sophia Anderson – Employee Relations Specialist (salary)
        (9, 62000, date(2017, 12, 11), None, 'salary'),

        # 10. Noah Thomas – Head of Mechanical Engineering (salary)
        (10, 95000, date(2016, 6, 30), None, 'salary'),

        # 11. Isabella Taylor – Project Manager (salary)
        (11, 70000, date(2019, 9, 15), None, 'salary'),

        # 12. Mason Moore – Project Manager (salary)
        (12, 72000, date(2015, 4, 2), date(2023, 12, 31), 'salary'),
        (12, 76000, date(2024, 1, 1), None, 'salary'),

        # 13. Mia Jackson – Mechanical Design Engineer (hourly)
        (13, 32, date(2022, 7, 19), None, 'hourly'),

        # 14. Ethan White – Manufacturing Engineer (salary)
        (14, 68000, date(2018, 10, 5), None, 'salary'),

        # 15. Amelia Harris – Quality Control Engineer (salary)
        (15, 66000, date(2020, 11, 3), None, 'salary'),

        # 16. Alexander Martin – Maintenance Engineer (hourly)
        (16, 27, date(2017, 2, 17), None, 'hourly'),

        # 17. Charlotte Garcia – Head of Network Operations (salary)
        (17, 88000, date(2021, 5, 27), None, 'salary'),

        # 18. Daniel Martinez – Project Manager (salary)
        (18, 69000, date(2019, 8, 13), None, 'salary'),

        # 19. Emily Rodriguez – Project Manager (salary)
        (19, 71000, date(2018, 1, 23), None, 'salary'),

        # 20. Matthew Lewis – Network Security Specialist (hourly)
        (20, 34, date(2022, 3, 29), None, 'hourly'),

        # 21. Abigail Walker – Network Technician (hourly)
        (21, 25, date(2020, 9, 10), None, 'hourly'),

        # 22. David Hall – Systems Analyst (salary)
        (22, 69000, date(2016, 12, 1), None, 'salary'),

        # 23. Elizabeth Allen – Telecommunications Specialist (hourly)
        (23, 29, date(2017, 7, 7), None, 'hourly'),

        # 24. Joseph Young – Head of Software Engineering (salary)
        (24, 95000, date(2019, 10, 16), None, 'salary'),

        # 25. Madison King – Project Manager (salary)
        (25, 72000, date(2021, 6, 14), None, 'salary'),

        # 26. Samuel Wright – Project Manager (salary)
        (26, 68000, date(2022, 1, 12), None, 'salary'),

        # 27. Ella Scott – Software Developer (hourly)
        (27, 31, date(2018, 4, 18), None, 'hourly'),

        # 28. Benjamin Green – QA Engineer (salary)
        (28, 63000, date(2020, 5, 22), None, 'salary'),

        # 29. Avery Adams – Technical Architect (salary)
        (29, 86000, date(2017, 3, 3), None, 'salary'),

        # 30. Jackson Baker – DevOps Engineer (salary)
        (30, 84000, date(2019, 11, 29), None, 'salary'),
    ]


    for emp_no, salary, start, end, sal_type in salary_records:
        emp_salary = EmployeeSalary(
            employee_no=emp_no,
            salary=salary,
            start_date=start,
            end_date=end,
            type=sal_type
        )
        db.session.add(emp_salary)

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