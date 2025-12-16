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
# install WSL using this command
# wsl --install

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
# How to run Streamlit App
- open a new terminal
- cd to your current root folder
- activate the environment
- run the command line in the terminal

''' bash
$ streamlit run app.py
'''
# To Give access to ngrok to open streamlit from browser
 $ streamlit run frontend.py --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false
### Run into ngrok
for windows
'''bash
$ ngrok http 8501 
'''
for wsl 
''' bash
$ ngrok.exe http 8501
'''
- copy the forwarding link like this: https://35c034e55843.ngrok-free.app
- open it in browser and try the app.



NOTE: To stop the Sever press CTRL + C



# Future Work 
- Save the History of the logining for each day
- Add a data validation to make it once login
- Improve the UI of the app using Another professional too than streamlit
- The user have the ability to add more info about him such as upload profile photo or take one , add connect with email address and phone number, position
- How to connect this app with real time camera using rasperiby 
- Recognize if this Image is Real or Fake to reduce cheating
- Deploye The model to Asure or AWS
- Modify the Data Base and make it more professional using SQLAlchmy
- Add Data Validation for the input that the user enter when he register for the first time for example First Name , Last Name , Password, email , etc..
- Give permessions For user and Admin when logging in so the admin could add new user and can access the attendance of each employee from it's dashboard by searching by the Id or name of employee
- Get the active working ours without leaving the office or playing 
