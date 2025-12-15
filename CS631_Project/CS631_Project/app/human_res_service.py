from datetime import date
from calendar import monthrange
from sqlalchemy import func, and_, or_
from .models import db, Employee, Department, Division, EmployeeSalary

def get_employees_with_salary():
    max_start_date_subq = (
        db.session.query(
            EmployeeSalary.employee_no,
            func.max(EmployeeSalary.start_date).label('max_start_date')
        )
        .group_by(EmployeeSalary.employee_no)
        .subquery()
    )
    max_id_subq = (
        db.session.query(
            EmployeeSalary.employee_no,
            func.max(EmployeeSalary.id).label('max_id')
        )
        .join(
            max_start_date_subq,
            and_(
                EmployeeSalary.employee_no == max_start_date_subq.c.employee_no,
                EmployeeSalary.start_date == max_start_date_subq.c.max_start_date
            )
        )
        .group_by(EmployeeSalary.employee_no)
        .subquery()
    )
    results = (
        db.session.query(Employee, Department, Division, EmployeeSalary)
        .join(Department, Employee.department_name == Department.department_name, isouter=True)
        .join(Division, Department.division_name == Division.division_name, isouter=True)
        .join(
            max_start_date_subq,
            Employee.employee_no == max_start_date_subq.c.employee_no,
            isouter=True
        )
        .join(
            max_id_subq,
            Employee.employee_no == max_id_subq.c.employee_no,
            isouter=True
        )
        .join(
            EmployeeSalary,
            and_(
                EmployeeSalary.employee_no == max_start_date_subq.c.employee_no,
                EmployeeSalary.start_date == max_start_date_subq.c.max_start_date,
                EmployeeSalary.id == max_id_subq.c.max_id
            ),
            isouter=True
        )
        .order_by(Employee.employee_no)
        .all()
    )
    employees = []
    for emp, dept, div, salary in results:
        employees.append({
            "employee_no": emp.employee_no,
            "employee_name": emp.employee_name,
            "title": emp.title,
            "department_name": dept.department_name if dept else '',
            "division_name": div.division_name if div else '',
            "employment_start_date": emp.employment_start_date,
            "employment_end_date": emp.employment_end_date,
            "is_active": emp.is_active,
            "salary": salary.salary if salary else None,
            "salary_start_date": salary.start_date if salary else None,
            "salary_type": salary.type if salary else None  # salary OR hourly
        })
    return employees