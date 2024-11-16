# -Code_Monkies-SOEN341_Project_F24-

# Peer Assessment System

## Overview
This project is a Peer Assessment Platform developed using Django. It allows students and instructors to manage assessments and evaluations efficiently. See the Wiki section for more details on the overall project, choice of technologies and team members. 

### Prerequisites
- Python 3.x
- Django
- Virtual Environment (recommended)

### Installation

1. **Clone the Repository**:
```bash
   git clone https://github.com/username/repository.git
   cd repository
```
2. **Create a Virtual Environment**
```bash
   python -m venv venv
```
3. **Activate the Virtual Environment**
On Windows
```bash
   venv\Scripts\activate
```
On Mac/Linux
```bash
   source venv/bin/activate
```
4. **Install Requirements using pip**
```bash
   pip install -r requirements.txt
```
5. **Run Migrations**
```bash
   python manage.py migrate
```
6. **Run the Development Server**
```bash
   python manage.py runserver
```
Note: to run the development server, you need to be in the same directory as the manage.py

### How to Use as a Student
To use the platform after the starting development server, open your preferred web browser and navigate to http://127.0.0.1:8000/

**Creating an Account**
To create an account, from the http://127.0.0.1:8000/ page, click on "Create an Account". Alternatively, you may go to the URL http://127.0.0.1:8000/register

**Logging in**
To login, from the http://127.0.0.1:8000/ page, enter your credentials and press the login button. This will bring you to your home page

**Viewing teammembers**
From the home page, click on the "View Teammates" button for a chosen team.

**Rating teammembers**
From the "Viewing Teammembers" page, select a teammate and a new page will appear. Enter your ratings and press submit.

**Viewing Ratings**
From the home page, click on the "View Ratings" button for a chosen team.

**Logging Out**
To logout, press the logout button at the top right of the page.

### How to Use as an Instructor
To use the platform after the starting development server, open your preferred web browser and navigate to http://127.0.0.1:8000/

**Creating an Account**
To create an account, from the http://127.0.0.1:8000/ page, click on "Create an Account". Alternatively, you may go to the URL http://127.0.0.1:8000/register

**Logging in**
To login, from the http://127.0.0.1:8000/ page, enter your credentials and press the login button. This will bring you to your home page

**Creating a Group**
To create a group, from the home page, click on the "Create Group" page. You may now either enter the names of students in the fields provided to insert students into a new group, or upload a CSV file. The CSV file must be in the following format:
   Group 1 Name,studentname,studentname,studentname,...
   Group 2 Name,studentname,studentname,studentname,...
   ....
   
**Viewing Ratings**
From the home page, click on the "View Ratings" button for a chosen team.


