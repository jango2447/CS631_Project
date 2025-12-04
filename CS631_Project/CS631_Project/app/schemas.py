
from marshmallow import Schema, fields

class EmployeeSchema(Schema):
    employee_no = fields.Int()
    employee_name = fields.Str()
    phone_number = fields.Str()
    title = fields.Str()
    department_name = fields.Str()

# Add other schemas for validation
