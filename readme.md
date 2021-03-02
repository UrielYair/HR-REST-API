# HR REST API Heading

instructions:
open up the terminal.

    git clone https://github.com/UrielYair/HR-REST-API.git
    cd HR-REST-API
    pip install -r requirement.txt

database creation/deletion - database already created - but if needed:
in terminal:

    python3
    from app import create_app
    from models.database import db
    db.create_all(app=create_app()) # in order to set up new database
    db.drop_all(app=create_app()) # in order to delete existing database
    exit()

## start server:

#### Option A:

in terminal:

    FLASK_APP=app.py
    flask run

#### Option B:

in terminal:

    python app.py

After running the server, open your browser and navigate to:
[Swagger Documentation](http://127.0.0.1:5000/apidocs/)

TECH Stack:

Python, flask, SQLAlchemy, SQLite, Marshmellow, flassger(swagger)

Full list of endpoints are written in swagger documentation:
http://127.0.0.1:5000/apidocs/

main endpoints:

GET
http://127.0.0.1:5000/api/skills/
http://127.0.0.1:5000/api/jobs/
http://127.0.0.1:5000/api/candidates/
http://127.0.0.1:5000/api/candidates_finder_by_job_id/{job_id}
http://127.0.0.1:5000/api/candidates_finder_by_job_title/{job_title}

POST
http://127.0.0.1:5000/api/skill/
http://127.0.0.1:5000/api/candidate/
http://127.0.0.1:5000/api/job/

feel free to use your favorite way of submitting http request:

-   cURL
-   postman
-   swagger UI

example using curl (available also in swagger):
skill:

    curl -i -H "Content-Type: application/json" -X POST -d '{"skill": "Python"}' http://localhost:5000/api/skill

candidate:

    curl -i -H "Content-Type: application/json" -X POST -d '{"candidate_name": "Uriel Yair", "candidate_skills": [ "Python", "Java", "React.js", "JavaScript" ]}' http://localhost:5000/api/candidate

job:

    curl -i -H "Content-Type: application/json" -X POST -d '{"job_title": "FrontEnd Engineer", "job_skills": [ "HTML2", "CSS", "JavaScript", "Sass" ]}' http://localhost:5000/api/job

![alt text](https://github.com/UrielYair/HR-REST-API/blob/master/swagger_apidocs.png?raw=true)
