from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base

ma = Marshmallow()
db = SQLAlchemy()
base = declarative_base()


class Project(db.Model):
    __tablename__ = 'project'

    int_user_id = db.Column(db.Integer, primary_key=True)
    str_username = db.Column(db.String(), nullable=False)
    str_mail = db.Column(db.String(), nullable=False)
    str_password = db.Column(db.String(), nullable=False)


class ProjectTeam(db.Model):
    __tablename__ = 'project_team'

    num_prjteam_id = db.Column(db.Numeric, primary_key=True)
    num_project_id = db.Column(db.Numeric, db.ForeignKey("project.num_project_id"), nullable=False)
    num_resource_id = db.Column(db.Numeric)
    str_resource_name = db.Column(db.Text)
    str_resource_type = db.Column(db.Text)
    str_modifiedby = db.Column(db.Text)
    dte_modifieddate = db.Column(db.DateTime)
    str_createdby = db.Column(db.Text)
    dte_createddate = db.Column(db.DateTime)


class ProjectSchema(ma.Schema):
    num_project_id = fields.Number(dump_only=True)
    str_project_cod = fields.String(required=True)
    str_prj_name = fields.String(required=True)
    str_description = fields.String()
    str_short_description = fields.String()
    num_cost = fields.Number()
    chr_status = fields.String()
    dte_initial_date = fields.Date()
    dte_end_date = fields.Date()
    num_prjtype_id = fields.Number()
    num_prjstatus_id = fields.Number()
    str_modifiedby = fields.String()
    dte_modifieddate = fields.DateTime()
    str_createdby = fields.String()
    dte_createddate = fields.DateTime()
