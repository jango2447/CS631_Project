from flask import Blueprint, jsonify

project_bp = Blueprint('project', __name__)

@project_bp.route('/projects')
def get_projects():
    # Placeholder for projects list
    return jsonify({'projects': []})
