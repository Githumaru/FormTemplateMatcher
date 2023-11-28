# FormTemplateMatcher
A Django application for seamless identification and validation of form data against predefined templates

# Overview

Form Matcher is a Python-based web application designed to identify and validate filled forms against a repository of predefined form templates.
It's equipped with the ability to match incoming form fields with established templates and dynamically type fields based on their values, ensuring accuracy and consistency in form processing.

# Installation

## Clone the repository to your local machine:
```
git clone https://github.com/Githumaru/FormTemplateMatcher.git
```

## Navigate to the project directory:
```
cd full_form
```

## Run the project using Docker Compose:
```
docker-compose up
```

### Open your web browser and go to http://localhost:8000 to access the application.

# Usage

Accessing the application: Once you have launched your web application, it will be accessible at http://localhost:8000 in your web browser.
There is a DB as a docker container with example data.
To search templates in db you can send a GET request to http://127.0.0.1:8000/get_form/ with the your form's parameters.
For example, http://127.0.0.1:8000/get_form/?field1=test@email.com&field2=message&field3=2023-11-23
