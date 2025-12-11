# Operational Digital Twin v1.1

![Build Status](https://github.com/fmlin0429712024/OperationalDigitalTwin/actions/workflows/firebase-deploy.yml/badge.svg)

A Proof of Concept for an Industrial Digital Twin, demonstrating Operational Intelligence (OI) and Business Intelligence (BI) using real-time simulated Edge Data.

## 🚀 Live Demo
**[Launch Dashboard](https://prescientdemos.web.app)** 

## 🏗️ Architecture
*   **Edge Simulator**: Python script generating realistic telemetry from 5 analytical instruments
*   **Cloud Database**: Firebase Firestore (NoSQL, real-time sync)
*   **Dashboard**: Streamlit web application hosted on Google Cloud Run
*   **CI/CD**: Automated deployment via GitHub Actions

## 📊 Features

### Operational Intelligence (OI)
- Real-time fleet monitoring dashboard
- Device health status tracking (Running/Idle/Error/Maintenance)
- Vibration and temperature anomaly detection
- Alert feed for critical events

### Business Intelligence (BI)
- Overall Equipment Effectiveness (OEE) calculation
- Utilization rate trending
- Revenue impact projections
- Operator performance insights

## 🎯 Inspired By

This PoC is based on the [Prescient Devices Customer Story](https://www.prescientdevices.com/customer-story/industrial-digital-twin-for-oi-and-bi) which achieved:
- ✅ 39% improvement in instrument utilization
- ✅ Complete visibility into installed base
- ✅ New SaaS revenue from Lab Insights software
- ✅ Reduced operator errors and downtime

## 📦 Local Development

### Prerequisites
- Python 3.9+
- Firebase project with Firestore enabled
- Service account key (for local development)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/fmlin0429712024/OperationalDigitalTwin.git
   cd OperationalDigitalTwin
   ```

2. **Install dependencies**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Configure Firebase**
   - Place your `serviceAccountKey.json` in the project root
   - Or use Application Default Credentials: `gcloud auth application-default login`

4. **Run locally**
   ```powershell
   # Option 1: Run both services together
   .\run_poc.ps1
   
   # Option 2: Run separately
   # Terminal 1 - Simulator
   python simulator.py
   
   # Terminal 2 - Dashboard
   streamlit run main.py
   ```

## 🚢 Deployment

The project uses automated CI/CD via GitHub Actions. Every push to `main` triggers:
1. Docker container build
2. Deployment to Google Cloud Run
3. Firebase Hosting update

See `.github/workflows/firebase-deploy.yml` for details.

## 📁 Project Structure

```
OperationalDigitalTwin/
├── main.py                 # Streamlit dashboard application
├── simulator.py            # Edge device simulator
├── firebase_config.py      # Firebase connection logic
├── start.sh               # Startup script for Cloud Run
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
├── firebase.json          # Firebase Hosting configuration
├── .firebaserc           # Firebase project settings
├── spec.md               # Technical specification
├── plan.md               # Implementation plan
├── tasks.md              # Development tasks
└── README.md             # This file
```

## 🔧 Technologies Used

- **Frontend**: Streamlit, Plotly
- **Backend**: Python, Firebase Admin SDK
- **Database**: Google Cloud Firestore
- **Hosting**: Google Cloud Run, Firebase Hosting
- **CI/CD**: GitHub Actions
- **Simulation**: Faker (synthetic data generation)

## 📝 License

This is a demonstration project for educational purposes.

## 🤝 Contributing

This is a PoC project. For questions or suggestions, please open an issue.

---

**Built with ❤️ to demonstrate the power of Digital Twin technology**
