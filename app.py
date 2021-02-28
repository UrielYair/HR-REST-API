from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


# Create instance of Flask class
app = Flask(__name__)
ma = Marshmallow(app)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///human_resources.sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##### MODELS #####

candidate_skills = db.Table(
    'candidate_skills',
    db.Column('candidate_id', db.Integer,
              db.ForeignKey('candidate.candidate_id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.skill_id'))
)

job_requirements = db.Table(
    'job_requirements',
    db.Column('job_id', db.Integer,
              db.ForeignKey('job.job_id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.skill_id'))
)


class Candidate(db.Model):
    # __tablename__ = 'candidates'
    candidate_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)

    skills = db.relationship(
        'Skill', secondary=candidate_skills,
        backref=db.backref('candidate', lazy='joined')
    )

    def __repr__(self):
        return '<Candidate %r %r>' % (self.title, self.skills)


class Job(db.Model):
    # __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)

    skills = db.relationship(
        'Skill', secondary=job_requirements,
        backref=db.backref('job', lazy='joined')
    )

    def __repr__(self):
        return '<Job %r>' % (self.title)


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

class CandidateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Candidate
        include_fk = True

    skills = ma.List(ma.HyperlinkRelated("skill_detail"))
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("candidate_detail", values=dict(id="<candidate_id>")),
            "collection": ma.URLFor("candidates"),
        }
    )


class JobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Job
        include_fk = True

    skills = ma.List(ma.HyperlinkRelated("skill_detail"))
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("job_detail", values=dict(id="<job_id>")),
            "collection": ma.URLFor("jobs"),
        }
    )


class SkillSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Skill
        include_fk = True

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("skill_detail", values=dict(id="<skill_id>")),
            "collection": ma.URLFor("skills"),
        }
    )


# Init schemas
candidate_schema = CandidateSchema()
candidates_schema = CandidateSchema(many=True)
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)


##### API #####

##### skills #####
@ app.route("/api/skills/")
def skills():
    all_skills = Skill.query.all()
    return jsonify(skills_schema.dump(all_skills))


@ app.route("/api/skills/<int:id>")
def skill_detail(id):
    skill = Skill.query.get_or_404(id)
    return skill_schema.dump(skill)


@ app.route('/api/skills/<string:skill_name>')
def show_skill(skill_name):
    found_skill = Skill.query.filter_by(name=skill_name).first_or_404(
        description='There is no data with - {}'.format(skill_name))
    return skill_schema.dump(found_skill)


@ app.route('/api/skill/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return skill_schema.dump(skill)


##### jobs #####

@ app.route("/api/jobs/")
def jobs():
    all_jobs = Job.query.all()
    return jsonify(jobs_schema.dump(all_jobs))


@ app.route("/api/jobs/<int:id>")
def job_detail(id):
    job = Job.query.get_or_404(id)
    return job_schema.dump(job)


@ app.route('/api/jobs/<string:job_title>')
def show_job(job_title):
    found_job = Job.query.filter_by(title=job_title).first_or_404(
        description='There is no data with - {}'.format(job_title))
    return job_schema.dump(found_job)


@ app.route('/api/job', methods=['POST'])
def job():

    # {
    # "job_title": "full-stack Developer",
    # "job_skills": [ "React.js", "JavaScript" ]
    # }

    # curl -i -H "Content-Type: application/json" -X POST -d '{"job_title": "FrontEnd Engineer1", "job_skills": [ "HTML2", "C33SS", "JadevaScript", "Sfffass" ]}' http://localhost:5000/api/job

    data = request.json

    new_job = Job(title=data["job_title"])

    for skill_name in data["job_skills"]:
        # Find skill in DB:
        skill = Skill.query.filter_by(name=skill_name).first()

        # check if skill already in DB:
        exists = skill is not None
        if not exists:
            skill = Skill(name=skill_name)  # Create new skill row in DB
            db.session.add(skill)           # store in DB:

        # add required skill to job opening
        new_job.skills.append(skill)

    db.session.add(new_job)
    db.session.commit()

    return job_schema.dump(new_job)


##### candidates #####

@ app.route("/api/candidates/")
def candidates():
    all_candidates = Candidate.query.all()
    return jsonify(candidates_schema.dump(all_candidates))


@ app.route("/api/candidates/<int:id>")
def candidate_detail(id):
    candidate = Candidate.query.get_or_404(id)
    return candidate_schema.dump(candidate)


@ app.route('/api/candidates/<string:candidate_title>')
def show_candidate(candidate_title):
    found_candidate = Candidate.query.filter_by(
        title=candidate_title).first_or_404(
        description='There is no data with - {}'.format(candidate_title))
    return candidate_schema.dump(found_candidate)


@ app.route('/api/candidate', methods=['POST'])
def candidate():

    # {
    # "candidate_name": "Uriel Yair",
    # "candidate_skills": [ "Python", "Java", "React.js", "JavaScript" ]
    # }

    # curl -i -H "Content-Type: application/json" -X POST -d '{"candidate_name": "Uriel Yair", "candidate_skills": [ "Python", "Java", "React.js", "JavaScript" ]}' http://localhost:5000/candidate

    data = request.json

    new_candidate = Candidate(title=data["candidate_name"])

    for skill_name in data["candidate_skills"]:
        # Find skill in DB:
        skill = Skill.query.filter_by(name=skill_name).first()

        # check if skill already in DB:
        exists = skill is not None
        if not exists:
            # Create new skill row in DB
            skill = Skill(name=skill_name)
            db.session.add(skill)               # store in DB

        # add required skill to job opening
        new_candidate.skills.append(skill)

    db.session.add(new_candidate)
    db.session.commit()

    return candidate_schema.dump(new_candidate)


@ app.route('/api/candidates_finder_by_job_title/<string:job_name>')
def find_candidate_by_job_name(job_name):
    job_to_find_candidates_for = Job.query.filter_by(
        title=job_name).first_or_404(job_name, description='job name not exist')
    skills_id = [
        skills_id.skill_id for skills_id in job_to_find_candidates_for.skills]

    return jsonify(candidates_schema.dump(get_skilled_candidates(skills_id)))


@ app.route('/api/candidates_finder_by_job_id/<int:job_id>')
def find_candidate_by_job_id(job_id):
    job_to_find_candidates_for = Job.query.get_or_404(
        job_id, description='job id not exist')
    skills_id = [
        skills_id.skill_id for skills_id in job_to_find_candidates_for.skills]

    return jsonify(candidates_schema.dump(get_skilled_candidates(skills_id)))


def get_skilled_candidates(skill_ids):
    # based on relational division.

    # SQL Relational Division:
    # https://www.youtube.com/watch?v=KJvo1XfiKPE
    # https://www.geeksforgeeks.org/sql-division/

    skills = db.union_all(*[
        db.select([db.literal(sid).label('skill_id')])
        for sid in skill_ids]).alias()

    return Candidate.query.\
        filter(
            ~db.exists().select_from(skills).where(
                ~db.exists().
                where(db.and_(candidate_skills.c.skill_id == skills.c.skill_id,
                              candidate_skills.c.candidate_id == Candidate.candidate_id)).
                correlate_except(candidate_skills))).\
        all()


##### Main #####
if __name__ == '__main__':
    app.run(debug=True)
