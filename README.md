# Challenge Stack
This application is a sample REST API for the challenge of handling transactions using a.csv file.

# Methodologies that were used

This API was built with the MVC architecture pattern,
also the Singleton pattern, since it manages the single instance of the class in charge of processing the file and sending emails. This ensures that there is only one instance of the class in the entire application, making it easier to globally access this functionality.
and SOLID principles specifically the SRP, OCP and ISP principles


# Getting started

So that you can quickly run through the challenge, some bootstrap scripts have been created to make things easier.

but first, download the file called settings.ini and add it to the root of the project
file link: https://drive.google.com/drive/folders/1UFdFpkwF4XY8xV4HV4SpNqkcD5_8AjKb?usp=sharing

> change the sender_email, recipient_email and email_password settings to your own settings so you can validate if you received the email.


---

In plain language, all you need to do is run bootstrap with make to build the container.


A detailed step-by-step description is:
```
make build
```
The development server should have started now. You can visit the API by navigating in a browser to: `http://0.0.0.0:8000/`


Once you finish installing the entire container and can access the url, open another terminal and generate the migrations for the project

A detailed step-by-step description is:
```
make migrate
```
This will generate migrations for your database.


### The next step is to create a superuser to send data to the API:

run the following command and create the test user with the credentials from the file: https://drive.google.com/drive/folders/1zdvVH7UC0t3Pw9vWksTiQ6a0d8ft8n6j?usp=sharing
the file called credentials.txt

```
make createsuperuser
```
And finally you can test the API by running the following command

```
make runCLI
```

* Remember that you must have created the user in the previous step, since the API will ask you to be an authenticated user

---


A guide on how to install docker for Linux, Mac and Windows is available here: https://docs.docker.com/get-docker/

Disclaimer: These instructions were tested using a Linux operating system, for Windows we suggest you install bash for Windows: https://itsfoss.com/install-bash-on-windows/

Python 3.10 was used to develop and test this challenge.

---

### You can run other commands to validate the state of the api:

* To verify the code with Pylint:

```
make qualityDocker
```


* To run the tests:
```
make test
```
