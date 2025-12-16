# Employee Attendance using Face Recognition
Taking the attendance of the employees using face recognition 
## Project Sturcture
sentinel_pro/
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/               # CORE: Config & Database Setup
│   │   ├── __init__.py
│   │   ├── config.py       # (Moved from app/config.py)
│   │   └── database.py     # (Moved from app/database.py)
│   │
│   ├── models/             # MODEL: Database Tables
│   │   ├── __init__.py
│   │   └── employee.py     # (Moved from app/models.py)
│   │
│   ├── services/           # SERVICE: The "Brain" (AI Logic)
│   │   ├── __init__.py
│   │   └── face_logic.py   # (Moved from app/services.py)
│   │
│   ├── controllers/        # CONTROLLER: API Endpoints (JSON)
│   │   ├── __init__.py
│   │   └── auth_controller.py  # Handles Register/Login APIs
│   │
│   ├── views/              # VIEW: Frontend Routes (HTML)
│   │   ├── __init__.py
│   │   └── home_view.py    # Serves the HTML pages
│   │
│   └── main.py             # ENTRY POINT: Wires everything together
│
├── static/                 # (CSS/JS - No changes)
├── templates/              # (HTML - No changes)
├── .env
└── environment.yml
# clone the repo

## Requirments

- python 3.10 or later

#### Install python using MiniConda
1) Download and install MiniConda from [here] (https://www.anaconda.com/docs/getting-started/miniconda/install#linux-terminal-installer)
2) create a new environment using the following commands:
```bash
$ conda env create -f environment.yml
```
3) Activate the environment:
$ conda activate employee_env

### Setup the enviroment variables

``` bash 
$ cp .env.example .env
```

set you environment variables in the `.env` file. Like 


### Run the FastApi Server
``` bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
NOTE: To stop the Sever press CTRL + C



# Create Virtual Enviroment 

# install WSL using this command
# wsl --install
