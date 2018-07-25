import logging as log
import requests
import json
import constants as cons
import os

from models import Project, ProjectTeam, db
from errors import ProjectControllerError, AppSecurityControllerError
from sqlalchemy.orm import exc
from sqlalchemy.exc import SQLAlchemyError


class AppSecurityController:

    def __init__(self):
        pass

    def get_password(self, user_auth):
        try:
            json_in = {'oauth_user': {'user': user_auth, 'password': None}}
            service_resp = requests.post(os.environ.get('URL_OAUTH_SECURITY_SERVICE'), json=json_in)

            log.debug('Response security service: {}'.format(service_resp.status_code))

            if service_resp.status_code is not cons.HTTP_200_OK:
                raise AppSecurityControllerError(service_resp.status_code)

            json_out = json.loads(service_resp.text)
            content = json_out.get('content')

            if content is None:
                raise AppSecurityControllerError(cons.SECURITY_RESPONSE_MSG)

            oauth_user = content.get('oauth_user')

            if oauth_user is None:
                raise AppSecurityControllerError(cons.SECURITY_RESPONSE_MSG)

            log.debug("end get password")

            return oauth_user.get('str_oauth_cred_password')
        except requests.RequestException as e:
            raise AppSecurityControllerError(e)


class ProjectController:

    def __init__(self):
        pass

    def select_by_id(self, project_id):
        s = db.session
        try:
            return s.query(Project).get(project_id)
        except exc.NoResultFound:
            log.info('Project with id {} was not found'.format(project_id))
            return None
        except SQLAlchemyError as e:
            log.error(str(e))
            raise ProjectControllerError(e)
        finally:
            s.close()

    def select_by_fields(self, conditionals):
        s = db.session
        try:
            query = s.query(Project)

            filters = None

            if bool(conditionals):
                listx = list()
                for key, val in conditionals.items():
                    listx.append(getattr(Project, key) == val)
                    log.debug('filter {} -> value {}'.format(key, val))

                filters = tuple(listx)

            query = query.all() if not filters else query.filter(*filters)
            return query
        except exc.NoResultFound:
            log.info('Project were not found')
            return None
        except SQLAlchemyError as e:
            log.error(str(e))
            raise ProjectControllerError(e)
        finally:
            s.close()

    def select_by_resource(self, resource_id):
        s = db.session
        try:
            return s.query(Project) \
                .filter_by(ProjectTeam.num_resource_id == resource_id).first()
        except exc.NoResultFound:
            log.info('Projects associated to resource_id {} were not found'.format(resource_id))
            return None
        except SQLAlchemyError as e:
            log.error(str(e))
            raise ProjectControllerError(e)
        finally:
            s.close()

    def insert(self, project):
        s = db.session
        try:
            log.info('Starting process')
            s = db.session
            s.add(project)
            s.commit()

            log.info('Project with id {} was inserted'.format(project.num_project_id))
            return project

        except SQLAlchemyError as e:
            log.error(str(e))
            raise ProjectControllerError(e)
        finally:
            s.close()

    def update(self, get_project):
        log.info('Updating project')
        s = db.session
        try:

            project = s.query(Project).filter(
                Project.num_project_id == get_project.num_project_id).with_for_update().one()

            project.str_prj_name = get_project.str_prj_name
            project.str_description = get_project.str_description
            project.str_short_description = get_project.str_short_description
            project.num_cost = get_project.num_cost
            project.chr_status = get_project.chr_status
            project.dte_initial_date = get_project.dte_initial_date
            project.dte_end_date = get_project.dte_end_date

            s.add(project)
            s.commit()

            log.info('Project with id {} was updated'.format(project.num_activity_id))

        except exc.NoResultFound:
            raise ProjectControllerError('Project with id {} was not found'.format(get_project.num_project_id))
        except SQLAlchemyError as e:
            log.error(str(e))
            raise ProjectControllerError(e)

        return project

    def remove(self, project_id):
        log.info('Removing project')
        s = db.session
        try:
            p = s.query(Project).get(project_id)
            s.delete(p)
            s.commit()
            log.info('Removed project: ' + str(p))
        except exc.NoResultFound:
            log.info('Project with id {} was not found'.format(project_id))
            raise ProjectControllerError('Project with id {} was not found'.format(project_id))
        except SQLAlchemyError as e:
            log.error(str(e))
            raise ProjectControllerError(e)
        finally:
            s.close()
