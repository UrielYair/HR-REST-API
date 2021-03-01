from models.database import db, ma
from models.linking_tables import job_requirements, candidate_skills

##### MODELS #####


class Job(db.Model):
    # __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)

    skills = db.relationship(
        'Skill', secondary=job_requirements,
        backref=db.backref('job', lazy='dynamic')
    )

    def __repr__(self):
        return '<Job %r>' % (self.title)


##### SCHEMAS #####


class JobSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Job
        include_fk = True

    skills = ma.List(ma.HyperlinkRelated("skill_blueprint.skill_detail"))
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("job_blueprint.job_detail", values=dict(id="<job_id>")),
            "collection": ma.URLFor("job_blueprint.jobs"),
        }
    )


# Init job schemas
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
