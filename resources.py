import logging as log
import constants as cons
import helpers

from flask import jsonify, request
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth
from webargs import fields
from webargs.flaskparser import use_args
from datetime import datetime

from models import Project, ProjectSchema
from controllers import ProjectController, AppSecurityController
from errors import ProjectControllerError, AppSecurityControllerError

auth = HTTPBasicAuth()
app_security_controller = AppSecurityController()
project_controller = ProjectController()
project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)

# parameters from url
url_args = {
    'num_project_id': fields.Number(),
    'num_resource_id': fields.Number()
}


@auth.get_password
def get_password(oauth_user):
    try:
        resp = app_security_controller.get_password(oauth_user)
        log.debug('type res: {}'.format(type(resp)))
        log.debug('sending password ...')
        return resp

    except AppSecurityControllerError as e:
        log.error(e)
        return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    resp = helpers.standar_response(cons.HTTP_403_FORBIDDEN, None, cons.SECURITY_UNAUTHORIZED_MSG)
    return jsonify(resp)


class ProjectResource(Resource):

    @auth.login_required
    def get(self, project_id):
        try:
            project = project_controller.select_by_id(project_id)
            project_serialized, project_errs = project_schema.dump(project)
            response = helpers.standar_response(cons.HTTP_200_OK, project_serialized, None)
            return response, cons.HTTP_200_OK

        except ProjectControllerError as e:
            log.error(e)
            response = helpers.standar_response(cons.HTTP_500_INTERNAL_SERVER_ERROR, None, e.message)
            return response, cons.HTTP_500_INTERNAL_SERVER_ERROR

    @auth.login_required
    def put(self, project_id):
        try:
            json_in = request.get_json(force=True)

            if json_in.get('project') is None:
                response = helpers.standar_response(cons.HTTP_400_BAD_REQUEST, None, cons.BAD_REQUEST_MSG)
                return response, cons.HTTP_400_BAD_REQUEST

            json = json_in['project']

            p = Project(
                num_project_id=project_id,
                num_project_cod=json.get('num_project_cod'),
                str_prj_name=json.get('str_prj_name'),
                str_description=json.get('str_description'),
                str_short_description=json.get('str_short_description'),
                num_cost=json.get('num_cost'),
                chr_status=json.get('chr_status'),
                dte_initial_date=json.get('dte_initial_date'),
                dte_end_date=json.get('dte_end_date'),
                num_prjtype_id=json.get('num_prjtype_id'),
                num_prjstatus_id=json.get('num_prjstatus_id'),
                str_modifiedby=json.get('str_modifiedby'),
                dte_modifieddate=json.get('dte_modifieddate'),
                str_createdby=json.get('str_createdby'),
                dte_createddate=json.get('dte_createddate')
            )

            project_controller.update(p)

            response = helpers.standar_response(cons.HTTP_200_OK, None, None)
            return response, cons.HTTP_200_OK

        except ProjectControllerError as e:
            response = helpers.standar_response(cons.HTTP_500_INTERNAL_SERVER_ERROR, None, e.message)
            return response, cons.HTTP_500_INTERNAL_SERVER_ERROR

    @auth.login_required
    def delete(self, project_id):
        try:
            project_controller.remove(project_id)

            response = helpers.standar_response(cons.HTTP_204_NO_CONTENT, None, None)
            return response, cons.HTTP_204_NO_CONTENT
        except ProjectControllerError as e:
            response = helpers.standar_response(cons.HTTP_500_INTERNAL_SERVER_ERROR, None, e.message)
            return response, cons.HTTP_500_INTERNAL_SERVER_ERROR


class ProjectListResource(Resource):

    @use_args(url_args)
    @auth.login_required
    def get(self, url_args):
        try:
            url_args = dict((k, v) for k, v in url_args.items() if v is not "")

            result = project_controller.select_by_fields(url_args)

            projects_serialized, projects_errs = projects_schema.dump(result)

            response = helpers.standar_response(cons.HTTP_200_OK, projects_serialized, None)
            return response, cons.HTTP_200_OK
        except ProjectControllerError as e:
            response = helpers.standar_response(cons.HTTP_500_INTERNAL_SERVER_ERROR, None, e.message)
            return response, cons.HTTP_500_INTERNAL_SERVER_ERROR

    @auth.login_required
    def post(self):
        log.info('inserting project ...')
        json_in = request.get_json(force=True)

        if json_in.get('project') is None:
            resp = helpers.standar_response(cons.HTTP_400_BAD_REQUEST, None, cons.BAD_REQUEST_MSG)
            return resp, cons.HTTP_400_BAD_REQUEST

        json = json_in['project']

        p = Project(
            num_project_cod=json.get('num_project_cod'),
            str_prj_name=json.get('str_prj_name'),
            str_description=json.get('str_description'),
            str_short_description=json.get('str_short_description'),
            num_cost=json.get('num_cost'),
            chr_status=json.get('chr_status'),
            dte_initial_date=json.get('dte_initial_date'),
            dte_end_date=json.get('dte_end_date'),
            num_prjtype_id=json.get('num_prjtype_id'),
            num_prjstatus_id=json.get('num_prjstatus_id'),
            str_createdby=json.get('str_createdby'),
            dte_createddate=datetime.utcnow()
        )

        project_controller.insert(p)

        project_serialized, project_err = project_schema.dump(p)

        log.info('project inserted!')

        content = {'project': project_serialized}

        response = helpers.standar_response(cons.HTTP_200_OK, content, None)
        return response, cons.HTTP_200_OK

    @auth.login_required
    def put(self):
        pass

    def delete(self):
        pass
