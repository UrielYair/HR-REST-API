open up the terminal.

git clone {repository}.
cd repo
pip install -r requirement.txt

open python interpreter by typing - python3
type the following commands:

from app import db
db.create_all()
exit()

start server:
FLASK_APP=app.py
flask run

TECH Stack:
Python, flask, SQLAlchemy, SQLite, Marshmellow, flassger(swagger)
apispec - for using marshmellow schema in flassger

Endpoints:
GET
http://127.0.0.1:5000/api/skills/
http://127.0.0.1:5000/api/candidates/
http://127.0.0.1:5000/api/jobs/
http://127.0.0.1:5000/api/candidates_finder_by_job_id/{job_id}
http://127.0.0.1:5000/api/candidates_finder_by_job_title/{job_title}

POST
http://127.0.0.1:5000/api/skill/
http://127.0.0.1:5000/api/candidate/
http://127.0.0.1:5000/api/job/

HTTP VERBS

skill
curl -i -H "Content-Type: application/json" -X POST -d '{"skill": "Python"}' http://localhost:5000/skill

candidadte
curl -i -H "Content-Type: application/json" -X POST -d '{"candidate_name": "Uriel Yair", "candidate_skills": [ "Python", "Java", "React.js", "JavaScript" ]}' http://localhost:5000/api/candidate

job
curl -i -H "Content-Type: application/json" -X POST -d '{"job_title": "FrontEnd Engineer", "job_skills": [ "HTML2", "CSS", "JavaScript", "Sass" ]}' http://localhost:5000/api/job
'''
