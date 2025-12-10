from flask import Blueprint, render_template, request, jsonify
from datetime import datetime, date
from calendar import monthrange
from sqlalchemy.orm import aliased
from sqlalchemy import func, and_, or_
from .models import db, Employee, Department, Division, EmployeeSalary

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    return render_template('index.html', title='Home Page', year=datetime.now().year)

@main_bp.route('/contact')
def contact():
    return render_template('contact.html', title='Contact', year=datetime.now().year, message='Your contact page.')

@main_bp.route('/about')
def about():
    return render_template('about.html', title='About', year=datetime.now().year, message='Your application description page.')

@main_bp.route('/test-template')
def test_template():
    return "<h1>Test route works!</h1>"

@main_bp.route('/human-resources')
def human_resources():
    # Subquery to get the latest salary record (by start date) for each employee
    latest_salary_subq = (
        db.session.query(
            EmployeeSalary.employee_no,
            func.max(EmployeeSalary.start_date).label('max_start_date')
        )
        .group_by(EmployeeSalary.employee_no)
        .subquery()
    )

    latest_salary = aliased(EmployeeSalary)

    # Query main HR data
    results = (
        db.session.query(Employee, Department, Division, latest_salary)
        .join(Department, Employee.department_name == Department.department_name, isouter=True)
        .join(Division, Department.division_name == Division.division_name, isouter=True)
        .join(
            latest_salary_subq,
            Employee.employee_no == latest_salary_subq.c.employee_no,
            isouter=True
        )
        .join(
            latest_salary,
            and_(
                latest_salary.employee_no == latest_salary_subq.c.employee_no,
                latest_salary.start_date == latest_salary_subq.c.max_start_date
            ),
            isouter=True
        )
        .filter(Employee.is_active == True)
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

    return render_template('human_resources.html', employees=employees)

@main_bp.route('/set-salary', methods=['POST'])
def set_salary():
    data = request.get_json()
    employee_no = data.get('employee_no')
    new_salary_str = data.get('new_salary')
    percent_increase_str = data.get('percent_increase')

    if not employee_no:
        return jsonify({'message': 'Employee number missing.'}), 400

    try:
        new_salary = float(new_salary_str) if new_salary_str else None
        percent_increase = float(percent_increase_str) if percent_increase_str else None
    except ValueError:
        return jsonify({'message': 'Invalid input for salary or percent increase.'}), 400

    if new_salary is None and percent_increase is None:
        return jsonify({'message': 'Please enter either a new salary or a percent increase.'}), 400

    current_salary_record = EmployeeSalary.query.filter_by(employee_no=employee_no, end_date=None).first()
    if not current_salary_record:
        return jsonify({'message': 'Current salary record not found.'}), 404

    current_salary = current_salary_record.salary

    if new_salary is None and percent_increase is not None:
        new_salary = current_salary * (1 + percent_increase / 100)
    if percent_increase is None and new_salary is not None:
        percent_increase = ((new_salary - current_salary) / current_salary) * 100

    # Update old salary record end_date
    current_salary_record.end_date = date.today()
    db.session.add(current_salary_record)

    # Add new salary record
    new_salary_record = EmployeeSalary(
        employee_no=employee_no,
        salary=new_salary,
        start_date=date.today(),
        end_date=None,
        type=current_salary_record.type
    )
    db.session.add(new_salary_record)

    db.session.commit()

    return jsonify({'message': f'Salary updated successfully for Employee #{employee_no}. New salary: ${new_salary:.2f} ({percent_increase:.2f}% increase)'}), 200


@main_bp.route('/salary-history/<int:employee_no>/<int:year>', methods=['GET'])
def salary_history(employee_no, year):
    # Get all salary records for employee that overlap with the year requested
    records = EmployeeSalary.query.filter(
        EmployeeSalary.employee_no == employee_no,
        EmployeeSalary.start_date <= date(year, 12, 31),
        or_(EmployeeSalary.end_date == None, EmployeeSalary.end_date >= date(year, 1, 1))
    ).order_by(EmployeeSalary.start_date).all()

    monthly_data = []

    for month in range(1, 13):
        month_start = date(year, month, 1)
        month_end = date(year, month, monthrange(year, month)[1])

        # Find the salary record that covers this month (latest by start_date)
        salary_record_for_month = None
        for record in records:
            rec_end = record.end_date or date.today()
            if record.start_date <= month_end and rec_end >= month_start:
                # Among candidates, pick the one with the latest start_date <= month_end
                if (salary_record_for_month is None or record.start_date > salary_record_for_month.start_date):
                    salary_record_for_month = record
        
        if salary_record_for_month:
            if salary_record_for_month.type == 'salary':
                monthly_salary = salary_record_for_month.salary / 12
            else:  # hourly
                monthly_salary = salary_record_for_month.salary * 160
        else:
            monthly_salary = 0

        fed_tax = monthly_salary * 0.10
        state_tax = monthly_salary * 0.05
        other_tax = monthly_salary * 0.03
        take_home = monthly_salary - (fed_tax + state_tax + other_tax)

        monthly_data.append({
            "month": month,
            "salary": round(monthly_salary, 2),
            "federal_tax": round(fed_tax, 2),
            "state_tax": round(state_tax, 2),
            "other_taxes": round(other_tax, 2),
            "take_home": round(take_home, 2)
        })

    return jsonify({
        "employee_no": employee_no,
        "year": year,
        "monthly_salary_history": monthly_data
    })
