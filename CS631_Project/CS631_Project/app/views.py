from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from .models import db, Employee

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

@main_bp.route('/human-resources')
def human_resources():
    employees = Employee.query.all()  # Fetch all employees from DB
    return render_template('human_resources.html', employees=employees)

@main_bp.route('/add-employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        # Retrieve form data
        employee_name = request.form.get('employee_name')
        phone_number = request.form.get('phone_number')
        title = request.form.get('title')
        department_name = request.form.get('department_name')

        # Create new Employee instance
        new_employee = Employee(
            employee_name=employee_name,
            phone_number=phone_number,
            title=title,
            department_name=department_name
        )

        # Add to DB and commit
        db.session.add(new_employee)
        db.session.commit()

        flash('Employee added successfully!', 'success')
        return redirect(url_for('main.human_resources'))

    # GET request renders the form template
    return render_template('add_employee.html')
