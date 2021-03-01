from models.database import db

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
