# CloudBank

- A Flask app that will eventually take an uploaded file, analyze it and post the results that can be viewed by the user who uploaded the file.

**State of the Current App**

- Application has a user signup and log in system implemented using a SQLite database.
- Login is required to upload files to s3 bucket for processing

**TODO**

- Create an AWS Lambda that will be triggered when a new file is uploaded to S3.
- Lambda will extract information about you information about file and make it available in a section that shows only what a user uploaded.
- Update homepage to provide more information about application

## Endpoints 

/signup

- user enters name, email and a password that will be used to authenticate user 

/login
- after signup users are routed to login screen to authenticate themselves and have access to other parts of the app

/create

- allows users to select a file from their computer and upload it to s3 after submission.
- Users can label the data as well as add a description that will be reflected on their homepage.
- S3 location is added to the database to allow for retrieval of file at a later time.

/update
- allows users to update the name of the data as well as the description provided when they uploaded the file.

/logout
- signs out the current user.

/view
- shows a list of user uploaded files with their names and time of upload and the option to edit

/
- sends user to homepage of application

