from flask import Flask
from flasgger import Swagger

from api.Skill.skill_blueprint import *
from api.Job.job_blueprint import *
from api.Candidate.candidate_blueprint import *


def create_app():
    app = Flask(__name__)

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///human_resources.sqlite.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # SQLAlchemy and Marshmallow
    from models.database import db, ma

    # SQLAlchemy and Marshmallow initiation:
    db.init_app(app)
    ma.init_app(app)

    ##### API #####
    # Blueprints registration
    app.register_blueprint(skill_blueprint, url_prefix="/api")
    app.register_blueprint(job_blueprint, url_prefix="/api")
    app.register_blueprint(candidate_blueprint, url_prefix="/api")

    #######################################
    from flasgger import APISpec, Schema, Swagger, fields
    from apispec.ext.marshmallow import MarshmallowPlugin
    from apispec_webframeworks.flask import FlaskPlugin

    # Create an APISpec
    spec = APISpec(
        title='HR REST API',
        version='1.0',
        openapi_version='2.0',
        plugins=[FlaskPlugin(), MarshmallowPlugin()]
    )

    from models.candidate import CandidateSchema
    from models.job import JobSchema
    from models.skill import SkillSchema

    template = spec.to_flasgger(
        app,
        definitions=[CandidateSchema, JobSchema, SkillSchema],
    )

    # set the UIVERSION to 3
    app.config['SWAGGER'] = {'uiversion': 3}

    # start Flasgger using a template from apispec
    swag = Swagger(app, template=template)
    #######################################

    return app


##### Main #####
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
