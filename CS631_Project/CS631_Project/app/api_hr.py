from flask import Blueprint, jsonify
from .models import db, Employee, Department, Division, EmployeeSalary

hr_bp = Blueprint('hr', __name__)

@hr_bp.route('/employees', methods=['GET'])
def get_employees():
    # Join employees  departments  divisions  titles
    employees = (
        db.session.query(Employee, Department, Division, EmployeeSalary)
        .join(Department, Employee.department_name == Department.department_name, isouter=True)
        .join(Division, Department.division_name == Division.division_name, isouter=True)
        .order_by(Employee.employee_no)
        .all()
    )

    results = []
    for emp, dept, div, title_info in employees:
        results.append({
            "employee_no": emp.employee_no,
            "name": emp.employee_name,
            "title": emp.title,
            "department": dept.department_name if dept else None,
            "division": div.division_name if div else None,
            "is_active": emp.is_active,
            "employment_start_date": (
                emp.employment_start_date.isoformat()
                if emp.employment_start_date else None
            ),
            "employment_end_date": (
                emp.employment_end_date.isoformat()
                if emp.employment_end_date else None
            ),
            "salary": title_info.salary if title_info else None,
        })

    return jsonify(results)
