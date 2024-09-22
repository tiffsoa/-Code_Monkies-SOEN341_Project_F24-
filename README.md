# -Code_Monkies-SOEN341_Project_F24-

# Peer Assessment System

## Overview
This project is a Peer Assessment Platform developed using Django. It allows students and instructors to manage assessments and evaluations efficiently. See the project README for more details on the overall project and team members. 

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

## Project Structure
SOEN341_Project/
│
├── mainApp/                
│   ├── migrations/       
│   ├── static/           
│   │   └── mainApp/
│   │       ├── css/
│   │       │   ├── page1.css          
│   │       │   ├── page2.css
|   |       |   └── page3.css        
│   │       └── images/
│   │           └── img1.png           
│   ├── templates/        
│   │   └── mainApp/
│   │       ├── page1.html
│   │       └── page2.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── SOEN341_Project/            
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py            
├── requirements.txt     
└── README.md             
