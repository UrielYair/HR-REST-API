from flask import Flask


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

    # blueprints
    from api.Skill.skill_blueprint import skill_blueprint
    from api.Job.job_blueprint import job_blueprint
    from api.Candidate.candidate_blueprint import candidate_blueprint

    ##### API #####
    # Blueprints registration
    app.register_blueprint(skill_blueprint, url_prefix="/api")
    app.register_blueprint(job_blueprint, url_prefix="/api")
    app.register_blueprint(candidate_blueprint, url_prefix="/api")

    return app


##### Main #####
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
