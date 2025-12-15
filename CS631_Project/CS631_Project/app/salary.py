from datetime import date
from .models import db, Employee, EmployeeSalary, SalaryPayment

def pay_salaries(payment_date: date = None):
    if payment_date is None:
        payment_date = date.today()

    employees = Employee.query.all()

    for emp in employees:
        # Find the salary for the employee's title
        title_record = EmployeeSalary.query.filter_by(title=emp.title).first()
        if not title_record:
            # Skip employees without a known salary title
            continue

        gross = title_record.salary
        federal_tax = gross * 0.10
        state_tax = gross * 0.05
        other_tax = gross * 0.03
        net_salary = gross - (federal_tax + state_tax + other_tax)

        # Create a new salary payment record
        payment = SalaryPayment(
            employee_no=emp.employee_no,
            payment_date=payment_date,
            gross_salary=gross,
            federal_tax=federal_tax,
            state_tax=state_tax,
            other_tax=other_tax,
            net_salary=net_salary,
        )

        db.session.add(payment)

    db.session.commit()
