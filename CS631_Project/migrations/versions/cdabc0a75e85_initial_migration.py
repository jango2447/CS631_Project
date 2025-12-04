"""Initial migration

Revision ID: cdabc0a75e85
Revises: 
Create Date: 2025-11-26 19:51:34.085571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cdabc0a75e85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables without foreign keys first to break cycles
    op.create_table('buildings',
        sa.Column('building_code', sa.String(length=10), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('year_bought', sa.Integer(), nullable=True),
        sa.Column('cost', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('building_code')
    )

    op.create_table('divisions',
        sa.Column('division_name', sa.String(length=50), nullable=False),
        sa.Column('employee_no', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('division_name')
    )

    op.create_table('departments',
        sa.Column('department_name', sa.String(length=50), nullable=False),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('division_name', sa.String(length=50), nullable=True),
        sa.Column('employee_no', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('department_name')
    )

    op.create_table('employees',
        sa.Column('employee_no', sa.Integer(), nullable=False),
        sa.Column('employee_name', sa.String(length=100), nullable=True),
        sa.Column('phone_number', sa.String(length=20), nullable=True),
        sa.Column('title', sa.String(length=50), nullable=True),
        sa.Column('department_name', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('employee_no')
    )

    op.create_table('projects',
        sa.Column('project_number', sa.Integer(), nullable=False),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('date_started', sa.Date(), nullable=True),
        sa.Column('date_ended', sa.Date(), nullable=True),
        sa.Column('manager_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('project_number')
    )

    op.create_table('rooms',
        sa.Column('office_number', sa.String(length=10), nullable=False),
        sa.Column('square_feet', sa.Float(), nullable=True),
        sa.Column('type', sa.String(length=20), nullable=True),
        sa.Column('building_code', sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint('office_number')
    )

    op.create_table('department_rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('department_name', sa.String(length=50), nullable=True),
        sa.Column('office_number', sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('employee_projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_no', sa.Integer(), nullable=True),
        sa.Column('project_number', sa.Integer(), nullable=True),
        sa.Column('hours_worked', sa.Float(), nullable=True),
        sa.Column('role', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('employee_rooms',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('employee_no', sa.Integer(), nullable=True),
        sa.Column('office_number', sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    # Add foreign key constraints separately to avoid circular dependency issues
    op.create_foreign_key('fk_divisions_employee', 'divisions', 'employees', ['employee_no'], ['employee_no'], use_alter=True)

    op.create_foreign_key('fk_departments_division', 'departments', 'divisions', ['division_name'], ['division_name'], use_alter=True)
    op.create_foreign_key('fk_departments_employee', 'departments', 'employees', ['employee_no'], ['employee_no'], use_alter=True)

    op.create_foreign_key('fk_employees_department', 'employees', 'departments', ['department_name'], ['department_name'], use_alter=True)

    op.create_foreign_key('fk_projects_manager', 'projects', 'employees', ['manager_id'], ['employee_no'], use_alter=True)

    op.create_foreign_key('fk_rooms_building', 'rooms', 'buildings', ['building_code'], ['building_code'], use_alter=True)

    op.create_foreign_key('fk_department_rooms_department', 'department_rooms', 'departments', ['department_name'], ['department_name'], use_alter=True)
    op.create_foreign_key('fk_department_rooms_room', 'department_rooms', 'rooms', ['office_number'], ['office_number'], use_alter=True)

    op.create_foreign_key('fk_employee_projects_employee', 'employee_projects', 'employees', ['employee_no'], ['employee_no'], use_alter=True)
    op.create_foreign_key('fk_employee_projects_project', 'employee_projects', 'projects', ['project_number'], ['project_number'], use_alter=True)

    op.create_foreign_key('fk_employee_rooms_employee', 'employee_rooms', 'employees', ['employee_no'], ['employee_no'], use_alter=True)
    op.create_foreign_key('fk_employee_rooms_room', 'employee_rooms', 'rooms', ['office_number'], ['office_number'], use_alter=True)


def downgrade():
    # Drop foreign keys first
    op.drop_constraint('fk_employee_rooms_room', 'employee_rooms', type_='foreignkey')
    op.drop_constraint('fk_employee_rooms_employee', 'employee_rooms', type_='foreignkey')

    op.drop_constraint('fk_employee_projects_project', 'employee_projects', type_='foreignkey')
    op.drop_constraint('fk_employee_projects_employee', 'employee_projects', type_='foreignkey')

    op.drop_constraint('fk_department_rooms_room', 'department_rooms', type_='foreignkey')
    op.drop_constraint('fk_department_rooms_department', 'department_rooms', type_='foreignkey')

    op.drop_constraint('fk_rooms_building', 'rooms', type_='foreignkey')

    op.drop_constraint('fk_projects_manager', 'projects', type_='foreignkey')

    op.drop_constraint('fk_employees_department', 'employees', type_='foreignkey')

    op.drop_constraint('fk_departments_employee', 'departments', type_='foreignkey')
    op.drop_constraint('fk_departments_division', 'departments', type_='foreignkey')

    op.drop_constraint('fk_divisions_employee', 'divisions', type_='foreignkey')

    # Drop tables in reverse order
    op.drop_table('employee_rooms')
    op.drop_table('employee_projects')
    op.drop_table('department_rooms')
    op.drop_table('rooms')
    op.drop_table('projects')
    op.drop_table('employees')
    op.drop_table('departments')
    op.drop_table('divisions')
    op.drop_table('buildings')
