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
- Enter the data base terminal
```bash
sudo -u postgres psql
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

# 🚀 Project Roadmap: EmpVision (v2.0)

This roadmap outlines the strategic development plan for **EmpVision**, moving from a foundational prototype to a robust, production-ready workforce intelligence system.

---

## Phase 1: Core Foundation & Data Integrity
> **Focus:** Strengthening the backend and database structure.

### 1. Professional Database Migration
* **Task:** Migrate from SQLite to PostgreSQL.
* **Why:** SQLite handles limited concurrency. PostgreSQL supports concurrent writes (critical for morning rush hours) and offers robust security features.
* **Tool:** SQLAlchemy with a PostgreSQL connector (local or hosted).

### 2. Advanced Input Validation
* **Task:** Implement strict Pydantic Schemas (v2) for registration.
* **Details:** Validate emails (regex), enforce strong password policies, and standardize phone numbers (E.164).

### 3. Expanded User Profile
* **Task:** Add schema columns for `Phone`, `Job Title`, `Email`, `Emergency Contact`, and `Profile Picture URL`.
* **Benefit:** Transforms the system into a searchable mini-HR directory.

---

## Phase 2: AI Core Overhaul & Intelligent Logic (Major Update ⚠️)
> **Focus:** Replacing legacy AI with a unified YOLOv8 pipeline, enabling video registration, and implementing business rules.

### 4. The "AI Engine" Consolidation (YOLO Integration)
* **Task:** Completely replace HOG and MTCNN with **YOLOv8 (Nano)**.
* **Why:** Unifies the tech stack into a single, high-performance model for both detection and enrollment. YOLOv8 offers superior robustness against side angles and low light compared to HOG.
* **Implementation:**
    * Remove `dlib` frontal detector and `MTCNN` dependencies.
    * Integrate `ultralytics` with `yolov8n-face.pt` for CPU-optimized inference.
    * **Pipeline:** YOLO Detection (Box & Landmarks) → Crop → Face Recognition (ResNet Embedding).

### 5. Smart Video Enrollment (The "Wow" Factor)
* **Task:** Upgrade the `/register` endpoint to support "Passive Video Registration" instead of static uploads.
* **Workflow:**
    1.  User initiates registration; UI opens a video stream.
    2.  **Auto-Capture:** System automatically extracts the **Best 5 Frames** based on centering, blur score (Laplacian Variance), and eye state (open).
    3.  **Upload:** Silently uploads the optimal frames to the backend.

### 6. Real-World Camera Connectivity (RTSP)
* **Task:** Update video capture code to accept **RTSP URLs** alongside webcam IDs.
* **Benefit:** Allows immediate testing with home IP cameras/security feeds, simulating real-world office conditions (latency, angles) early.

### 7. Smart Attendance Logic & RBAC
* **Task:** Implement "Check-In/Check-Out" state machine and Role-Based Access Control.
* **Logic:**
    * **First Scan:** Check-In.
    * **Subsequent Scans:** Check-Out (with debounce/cooldown logic).
* **Permissions:** Employee (View Own) vs. Admin (View All/Export).

---

## Phase 3: Security & Anti-Spoofing (Critical)
> **Focus:** Hardening the system against spoofing attacks.

### 8. Liveness Detection
* **Task:** Detect presentation attacks (photos/screens).
* **Method:**
    * **Active:** Challenge-response (e.g., "Blink now").
    * **Passive:** Texture/Frequency analysis to detect screen pixelation.
* **Tool:** Leverage YOLO landmarks for blink detection or integrate Silent-Face-Anti-Spoofing.

---

## Phase 4: Scaling the Interface (Frontend Upgrade)
> **Focus:** Transitioning to a professional Single Page Application (SPA).

### 9. React/Next.js Migration
* **Task:** Rebuild the frontend using React.js or Next.js.
* **Why:** Enables a responsive, "app-like" experience with smoother video handling and custom branding compared to Streamlit.
* **Note:** The backend API remains stable; the frontend simply consumes the existing JSON endpoints.

---

## Phase 5: Deployment & Edge Computing
> **Focus:** Production deployment and hardware integration.

### 10. Cloud Deployment
* **Task:** Dockerize backend (FastAPI) and database (PostgreSQL). Deploy to cloud infrastructure (AWS EC2/Lambda + RDS + S3 for images).

### 11. Hardware Integration (Raspberry Pi)
* **Task:** Deploy the detection module to a Raspberry Pi 5 at the "edge."
* **Architecture:** Pi runs the optimized YOLOv8n model locally. It transmits only face embeddings or cropped metadata to the cloud for verification, minimizing bandwidth.

---

## Future Enhancements
* **Model Optimization:** Evaluate newer architectures like **YOLOv12** or **RetinaFace** for specific long-range detection needs (e.g., large halls) if Phase 2 testing reveals limitations.

**Author:** [Tamer Elkot](https://www.google.com/search?q=https://github.com/tamer-elkoT) | **License:** EmpVision