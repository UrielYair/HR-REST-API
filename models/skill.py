from models.database import db, ma
from models.linking_tables import job_requirements, candidate_skills

##### MODELS #####


class Skill(db.Model):
    # __tablename__ = 'skills'
    skill_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    jobs = db.relationship(
        'Job', secondary="job_requirements", backref='job_skill', lazy="dynamic")
    candidates = db.relationship(
        'Candidate', secondary="candidate_skills", backref='candidate_skill', lazy="dynamic")

    def __repr__(self):
        return '<Skill %r>' % self.name


##### SCHEMAS #####

class SkillSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Skill
        fields = ('skill_id', 'name', 'links', 'skills')
        include_fk = True

    links = ma.Hyperlinks(
        {
            "self": ma.URLFor("skill_blueprint.skill_detail", values=dict(id="<skill_id>")),
            "collection": ma.URLFor("skill_blueprint.skills"),
        }
    )


# Init skill schemas
skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)
