# Messaging REST API
A simple Messaging REST API. Allows to:<br>
Register, Login, Logout, Send a message,<br>
Get messages, Get unread messages, <br>
Read a message and Delete a message<br>
<br>
The service is deployed on AWS EC2 machine @ http://18.191.193.129:8080/<br>
Load the postman collection and read the documentation to learn the usage.<br>
<br>
How to run locally on linux:
- Open terminal and cd to the repo dir.
- Install requirements: `$ pip3 install -r requirements.txt`
- Set environment to our flask app: `$ export FLASK_APP=app`
- Set environment to 'production' or skip to use 'development': `$ export FLASK_ENV=production`
- Initiate the db: `$ flask init-db`
- Run the app: `$ flask run`
