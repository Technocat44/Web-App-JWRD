# Web-App-JWRD

Team repo for CSE 312 Web App project

Notes:

Hey everyone. In order to make this as seamless as possible, make sure to install these packages on your local machine.

1. pip install flask
2. pip install flask-login
3. pip install flask-pymongo
4. pip install pythondns
5. pip install dotenv

Some useful readings:

Application Factories:
https://flask.palletsprojects.com/en/2.1.x/patterns/appfactories/

Views and Blueprints:
https://flask.palletsprojects.com/en/2.0.x/tutorial/views/#:~:text=A%20view%20function%20is%20the,turns%20into%20an%20outgoing%20response.

Flask-PyMongo docs:
https://flask-pymongo.readthedocs.io/en/latest/

Mongo-Atlas Set-Up:
https://www.freecodecamp.org/news/get-started-with-mongodb-atlas/


Workflow tips:

IMPORTANT: To run everything locally there will be some commands that need to be commented out.

1. Start by pulling the most recent repo from Github.
2. Create a branch to work on.
   - git branch "branch name"
   - git checkout "branch name" || - git checkout -b "branch name" does the same thing
3. Work on the branch and write some code.
4. git add, commit
5. Switch back to the main branch
   - git checkout main || git switch main
6. Merge the changes to main
   - git merge "branch name"
7. Then push the changes
   - git push
