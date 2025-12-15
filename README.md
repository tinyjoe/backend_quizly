# backend_quizly

A RESTful backend service for a platform for AI generated quizzes out of a YouTube video link..


## Django Project

The project is called 'backend_quizly', but project files are stored in the 'core' folder. Please refer to 'core/settings.py' for further details.


## Requirements

+ Python 3.13
+ Django 5.2.4
+ SQLite 3
+ yt-dlp 2025.12.08
+ Google Genai 1.53.0


## Technologies

backend_quizly uses the following technologies and tools: 

![Python](	https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)     ![Django](https://img.shields.io/badge/Django-5.2.4-green?style=for-the-badge&logo=django&logoColor=white)     ![DjangoREST](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)     ![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite&logoColor=white)      ![yt-dlp version](https://img.shields.io/github/v/release/yt-dlp/yt-dlp?label=yt-dlp&style=flat-square&color=blue&logo=youtube)     ![Google Gemini](https://img.shields.io/badge/google%20gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)   


## Django Apps

Apps include: 

+ auth_app - this is for signup and login logic with access and refresh token generated with simple jwt
+ quizly_app - this is for the data models of Quiz and Question and the logic for generating a quiz from a Youtube video, updating, viewing and deleting data with different permissions. Can only be accessed by authenticated users.


## Database

The SQLite3 database used sits in the Django project root folder. It is not included within the Git repo, so must instead be requested from the system admin. 


## Settings

There is 1 settings related file:

+ `settings.py` (for general project settings, regardless of environment and containing publicly accessible information)


## Installation

Clone the repostiory:
```sh
git clone https://github.com/tinyjoe/backend_quizly.git
cd backend_quizly
```

Create a virtual environment
```sh
python -m venv env
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install dependencies
```sh
pip install -r requirements.txt
```

## Database Migrations

Run the initial migrations
```sh
python manage.py migrate
```

When you make changes to models
```sh
python manage.py makemigrations
python manage.py migrate
```

## Start Development Server
```sh
python manage.py runserver
```

## Set the Gemini API Key
exchange the Gemini API Key in settings.py 
```sh
GEMINI_API_KEY = <your-api-key>
```

