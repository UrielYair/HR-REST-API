from models.database import db, ma
from models.linking_tables import job_requirements, candidate_skills

##### MODELS #####


class Candidate(db.Model):
    # __tablename__ = 'candidates'
    candidate_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)

    skills = db.relationship(
        'Skill', secondary=candidate_skills,
        backref=db.backref('candidate', lazy='dynamic')
    )

    def __repr__(self):
        return '<Candidate %r %r>' % (self.title, self.skills)


##### SCHEMAS #####

class CandidateSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Candidate
        include_fk = True

    skills = ma.List(ma.HyperlinkRelated("skill_blueprint.skill_detail"))
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("candidate_blueprint.candidate_detail", values=dict(id="<candidate_id>")),
            "collection": ma.URLFor("candidate_blueprint.candidates"),
        }
    )


# Init candidate schemas
candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)
