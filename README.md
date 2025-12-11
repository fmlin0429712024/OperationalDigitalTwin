# Operational Digital Twin PoC

![Build Status](https://github.com/fmlin0429712024/OperationalDigitalTwin/actions/workflows/firebase-deploy.yml/badge.svg)

A Proof of Concept for an Industrial Digital Twin, demonstrating Operational Intelligence (OI) and Business Intelligence (BI) using Simulated Edge Data.

## 🚀 Live Demo
**[Launch Dashboard](https://prescientdemos.web.app)** 

## 🏗️ Architecture
*   **Edge**: Python Simulator (`simulator.py`) generating telemetry.
*   **Cloud**: Firebase Firestore (NoSQL Database).
*   **App**: Streamlit Dashboard hosted on Google Cloud Run.

## 📦 How to Run Locally

1.  **Install Dependencies**:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

2.  **Service Account**:
    Ensure `serviceAccountKey.json` is in the root directory.

3.  **Run**:
    ```powershell
    .\run_poc.ps1
    ```
    Or manually:
    ```bash
    # Terminal 1
    python simulator.py
    
    # Terminal 2
    streamlit run main.py
    ```
