from flask import Blueprint, jsonify, request

from models.candidate import Candidate, CandidateSchema, candidate_schema, candidates_schema
from models.job import Job, JobSchema, job_schema, jobs_schema
from models.skill import Skill, SkillSchema, skill_schema, skills_schema

from models.database import db, ma
from models.linking_tables import job_requirements, candidate_skills

skill_blueprint = Blueprint('skill_blueprint', __name__)


##### skills #####
@ skill_blueprint.route("/skills/")
def skills():
    all_skills = Skill.query.all()
    return jsonify(skills_schema.dump(all_skills))


@ skill_blueprint.route("/skills/<int:id>")
def skill_detail(id):
    skill = Skill.query.get_or_404(id)
    return skill_schema.dump(skill)


@ skill_blueprint.route('/skills/<string:skill_name>')
def show_skill(skill_name):
    found_skill = Skill.query.filter_by(name=skill_name).first_or_404(
        description='There is no data with - {}'.format(skill_name))
    return skill_schema.dump(found_skill)


@ skill_blueprint.route('/skill/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    return skill_schema.dump(skill)
