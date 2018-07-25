from flask import Blueprint
from flask_restful import Api
from resources import ProjectResource, ProjectListResource

vfquiz_bp = Blueprint('users', __name__)
api = Api(vfquiz_bp)

# Route
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:users_id>')
