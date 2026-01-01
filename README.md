# 🛡️ EmpVison: AI Face Attendance System

**EmpVision** is a robust, AI-powered biometric attendance system designed to streamline employee check-ins using facial recognition. It combines a high-performance **FastAPI** backend with a user-friendly **Streamlit** dashboard, utilizing hybrid detection (MTCNN + HOG) for optimal speed and accuracy.

---

## 📂 Project Structure

The project follows a scalable **MVC (Model-View-Controller)** architecture to ensure clean code separation and maintainability.

```text
EmpyVision/
│__ .streamlit
    |__ config.toml
├── app/
│   ├── __init__.py
│   ├── core/               # ⚙️ Config & Database connection
│   │   ├── config.py
│   │   └── database.py
│   ├── models/             # 🗄️ Database Schemas (SQLAlchemy)
│   │   └── employee.py
│   ├── services/           # 🧠 AI Logic (Face Recognition & Detection)
│   │   └── face_logic.py
│   ├── controllers/        # 🎮 API Route Handlers
│   │   └── auth_controller.py
│   └── main.py             # 🚀 Application Entry Point
│
├── frontend.py             # 🎨 Streamlit Dashboard (The UI)
├── .env                    # 🔒 Environment Variables
├── environment.yml         # 📦 Conda Dependencies
└── README.md               # 📖 Documentation

```

---

## ⚡ Prerequisites

Before you begin, ensure you have the following installed:

* **Python 3.10+**
* **WSL 2** (Windows Subsystem for Linux) - Recommended for Windows users.
```bash
wsl --install

```


* **MiniConda** or **Anaconda** for environment management.

---

## 🛠️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Employee-Attendance-System.git
cd Employee-Attendance-System


```

### 2. Set Up the Environment

We use `conda` to manage dependencies strictly.

```bash
# Create the environment from file
conda env create -f environment.yml

# Activate the environment
conda activate Employee-Attendance-System

```
### To update a new package or framework after adding it to YML file 
```bash
conda env update -f environment.yml --prune
```
### (Optional) To know the name the Conda Environment that you have created so you can activate it directly run this code in Ubuntu Terminal :
```bash
conda env list
```

### 3. Configure Environment Variables

Create your secret configuration file.

```bash
cp .env.example .env

```

*Open `.env` and configure your database URL or secret keys as needed.*

---

## 🚀 Usage Instructions

To run the full system, you will need **two separate terminals**.

### Terminal 1: The Backend (FastAPI)

This powers the API and AI processing engine.

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```

*Server will start at `http://localhost:8000*`

### Terminal 2: The Frontend (Streamlit)

This launches the visual dashboard for users.

```bash
streamlit run frontend.py

```

*Dashboard will open automatically in your browser.*

---

## 🌐 Remote Access (Ngrok)

If you want to test the app on a mobile device or share it with a friend, use **ngrok**.

**1. Launch Streamlit with Remote Flags**
*(In Terminal 2, stop the previous command and run this instead)*

```bash
streamlit run frontend.py --server.port=8501 --server.enableCORS=false --server.enableXsrfProtection=false

```

**2. Start the Tunnel**
*(Open a 3rd Terminal)*

**For Windows (CMD/PowerShell):**

```bash
ngrok http 8501

```

**For WSL (Linux):**

```bash
ngrok.exe http 8501

```

**3. Access the Link**
Copy the `https://...` link provided by ngrok (e.g., `https://35c034e5.ngrok-free.app`) and open it on any device.

---

## 🔮 Future Roadmap

We are constantly improving Sentinel Pro. Here is what's coming next:

* **📊 Advanced Analytics:** Save and visualize detailed login history logs.
* **🛡️ Anti-Spoofing:** "Liveness detection" to prevent photo-based cheating.
* **🔐 Role-Based Access:** Admin dashboard for managing users vs. standard employee view.
* **📱 Enhanced UI:** Transitioning to a modern React/Next.js frontend.
* **☁️ Cloud Deployment:** Deployment scripts for AWS and Azure.
* **👁️ IoT Integration:** Real-time surveillance mode using Raspberry Pi.
* **✅ Data Validation:** Pydantic schemas for strict input validation during registration.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any features or bug fixes.

# Create a new release
```bash
git tag -a v0.1.0 -m "Initial working version (SQLite, basic structure)"
git push origin v0.1.0
```
# Create a new branch for development phase 1 called (develop)
1- Ensure the current branch
```bash
git branch
```
2- create new branch called >> develop
```bash
git checkout -b develop
```
3- push the new branch into github
```bash
git push origin develop
```
## Note: while we still working on (phase 1) we work on (develop) branch.
# After we finish it do these steps:
1- Ensure that I'm on the develop branch while I'm working on phase 1
```bash
git checkout develop
```
2- work as usual and add the changes and commit it as usual 
```bash 
git add .
git commit -m "Phase 1 – Core Foundation"
```
3- After Finishing Phase 1 
- Go back to the (main) branch.
```bash 
git checkout main
```
- Merge the (develop) branch to the (main) branch.
Go to github UI and press the Pull Request button.
OR from terminal(optional):
```bash
git merge develop
```
- Create a new release
```bash
git tag -a v0.2.0 -m "Phase 1 - Core Foundation Complete"
git push origin v0.2.0
```

---
## Releases
- v0.1.0: Initial working version (SQLite)
- v0.2.0: Phase 1 – Core Foundation

# Note 
Releases = Milestones

Branches = Work in Progress

# Phases
## Phase 1: Core Foundation & Data Integrity
Focus: Strengthening the backend and database structure.
1.	Professional Database Migration:
- Task: Migrate from SQLite to PostgreSQL.
- Why: SQLite is for testing. PostgreSQL handles concurrent users (hundreds of employees logging in at 9 AM) and offers better security.
- Tool: Continue using SQLAlchemy but connect it to a PostgreSQL instance.
2.	Advanced Input Validation:
- Task: Implement strict Pydantic Schemas for registration.
- Details: Validate emails (regex), enforce password strength, and ensure phone numbers follow international formats.- 3.	Expanded User Profile:
- Task: Add columns for Phone, Position, Email, Emergency Contact, and Profile Picture URL.
- Benefit: Allows HR/Admins to use the system as a mini-HR directory.
## Phase 2: Business Logic & Rules
Focus: Converting raw data into useful attendance reports.
4.	Role-Based Access Control (RBAC):
- Task: Create two permission levels:
	- Employee/Student: Can only view their own history.
	- Admin/HR: Can add users, view everyone's data, search by ID/Name, and export reports.
5.	Smart Attendance Logic:
-Task: "One Login Per Day" & "Working Hours Calculation."
-Logic:
	- First Scan (9:00 AM): Mark as "Check-In".
	- Subsequent Scans: Mark as "Already In" (Prevent duplicate logs) OR treat as "Check-Out" if scanning to leave.
	- Calculation: Working Hours = Last Check-Out Time - First Check-In Time.
## Phase 3: Security & Anti-Spoofing (Critical)
Focus: Preventing students or employees from cheating using photos/videos.
6.	Liveness Detection (Anti-Spoofing):
- Task: Detect if the camera is seeing a real face or a phone screen/printed photo.
- Method: Use "Blink Detection" (ask user to blink) or "Texture Analysis" (AI models that detect pixelation from screens).
- Recommendation: Use Silent Face Anti-Spoofing libraries or depth-sensing cameras.
## Phase 4: Scaling the Interface (Frontend Upgrade)
Focus: Making it look like a real SaaS product.
7.	Replace Streamlit with React/Next.js:
- Task: Rebuild the frontend using React.js (or Next.js).
- Why: Streamlit is great for data apps, but it is slow for consumer apps. React allows for custom branding, faster animations, and mobile responsiveness.
-	API: Your FastAPI backend remains exactly the same; React just consumes the JSON APIs.
## phase 5: Deployment & Hardware (Edge Computing)
Focus: Moving from laptop to the real world.
8.	Cloud Deployment:
-	Task: Deploy the Backend (FastAPI + DB) to AWS (EC2 or Lambda) or Azure.
-	Storage: Save user profile photos to AWS S3 buckets instead of the database.
9.	Hardware Integration (Raspberry Pi):
-	Task: Run the "Detection" code on a Raspberry Pi 4/5 mounted at the office door.
-	Architecture: The Pi does the face scanning (Edge) and sends only the result (or the face encoding) to the Cloud Server to verify.

# installing Postgresql in ubuntu terminal
```bash
sudo apt update
sudo apt upgrade -y
sudo apt install postgresql postgresql-contrib -y
```
- check that postgresql is installed
```bash
sudo systemctl status postgresql
```
##### create password 
```bash
\password postgres
```
insert you password twice

Create The Data base
```bash
CREATE DATABASE "EmpVision";
```
Quit

```bash
\q
```




**Author:** [Tamer Elkot](https://www.google.com/search?q=https://github.com/tamer-elkoT) | **License:** EmpVision