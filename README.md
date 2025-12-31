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

---

**Author:** [Tamer Elkot](https://www.google.com/search?q=https://github.com/tamer-elkoT) | **License:** EmpVision