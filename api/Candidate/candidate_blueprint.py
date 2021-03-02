from flask import Blueprint, jsonify, request

from models.candidate import Candidate, CandidateSchema, candidate_schema, candidates_schema
from models.job import Job, JobSchema, job_schema, jobs_schema
from models.skill import Skill, SkillSchema, skill_schema, skills_schema

from models.database import db, ma
from models.linking_tables import job_requirements, candidate_skills

from flasgger import swag_from

candidate_blueprint = Blueprint('candidate_blueprint', __name__)

##### candidates #####


@ candidate_blueprint.route("/candidates/")
@ swag_from('candidates.yaml')
def candidates():
    all_candidates = Candidate.query.all()
    return jsonify(candidates_schema.dump(all_candidates))


@ candidate_blueprint.route("/candidates/<int:id>")
@ swag_from('candidate_detail.yaml')
def candidate_detail(id):
    candidate = Candidate.query.get_or_404(id)
    return candidate_schema.dump(candidate)


@ candidate_blueprint.route('/candidates/<string:candidate_title>')
@ swag_from('show_candidate.yaml')
def show_candidate(candidate_title):
    found_candidate = Candidate.query.filter_by(
        title=candidate_title).first_or_404(
        description='There is no data with - {}'.format(candidate_title))
    return candidate_schema.dump(found_candidate)


@ candidate_blueprint.route('/candidate', methods=['POST'])
@ swag_from('candidate.yaml')
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


@ candidate_blueprint.route('/candidates/find_by_job_title/<string:job_name>')
@ swag_from('find_candidate_by_job_name.yaml')
def find_candidate_by_job_name(job_name):
    job_to_find_candidates_for = Job.query.filter_by(
        title=job_name).first_or_404(job_name, description='job name not exist')
    skills_id = [
        skills_id.skill_id for skills_id in job_to_find_candidates_for.skills]

    return jsonify(candidates_schema.dump(get_skilled_candidates(skills_id)))


@ candidate_blueprint.route('/candidates/find_by_job_id/<int:job_id>')
@ swag_from('find_candidate_by_job_id.yaml')
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
