# ResultsPDF
Send Email to a user if no data received for 5 minutes from user

The project is using Token based authentication with TokenAuthentication class provided
by Django Rest Framework.

For testing purposes, one can generate the token using below command in terminal in the 
project directory:
./manage.py drf_create_token <username>
for generating a fresh new token:
./manage.py drf_create_token -r <username>

Redis is being used both as a message_queue and an in-memory database.
Sending Email task is pushed to the celery through redis as the celery broker
and urls data to be sent to the user in email is stored in key-value pairs in redis db.

Endpoint for syncing data:
'http://localhost:8000/api/v1/generatePDF/data-sync'
required Headers:
Authorization: 'Token <generated_token>'
sample_request_body:
[
    "https://www.google.com",
	"https://www.youtube.com"
] 

For subsequent new requests before sending the email, data is synced in the redis db
and the subsequent scheduled celery tasks during each data-sync request check for the
change in data.
If data is changed, then no mail is sent. Else the email with the pdf containing 
suggested links is sent.

.env file with necessary variables will be required to run the project.