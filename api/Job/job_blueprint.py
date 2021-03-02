from flask import Blueprint, jsonify, request

from models.candidate import Candidate, CandidateSchema, candidate_schema, candidates_schema
from models.job import Job, JobSchema, job_schema, jobs_schema
from models.skill import Skill, SkillSchema, skill_schema, skills_schema

from models.database import db, ma
from models.linking_tables import job_requirements, candidate_skills

from flasgger import swag_from

job_blueprint = Blueprint('job_blueprint', __name__)

##### jobs #####


@ job_blueprint.route("/jobs/")
@ swag_from('jobs.yaml')
def jobs():
    all_jobs = Job.query.all()
    return jsonify(jobs_schema.dump(all_jobs))


@ job_blueprint.route("/jobs/<int:id>")
@ swag_from('job_detail.yaml')
def job_detail(id):
    job = Job.query.get_or_404(id)
    return job_schema.dump(job)


@ job_blueprint.route('/jobs/<string:job_title>')
@ swag_from('show_job.yaml')
def show_job(job_title):
    found_job = Job.query.filter_by(title=job_title).first_or_404(
        description='There is no data with - {}'.format(job_title))
    return job_schema.dump(found_job)


@ job_blueprint.route('/job', methods=['POST'])
@ swag_from('job.yaml')
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
