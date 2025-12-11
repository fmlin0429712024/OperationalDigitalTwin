# Implementation Plan: Operational Digital Twin PoC

This plan follows the specifications defined in `spec.md`. It is designed to be executed sequentially, building the "Edge" simulation first, followed by the "Cloud" data ingestion, and finally the "user-facing" Dashboard.

## Phase 1: Environment & Infrastructure Setup
**Goal**: Establish a stable development environment and secure connectivity to Firebase.
1.  **Project Initialization**: Set up Python virtual environment and Git integration.
2.  **Dependency Management**: Define `requirements.txt` with `streamlit`, `firebase-admin`, `pandas`, `plotly`, `faker`.
3.  **Firebase Integration**:
    *   Set up the Firebase Admin SDK.
    *   Create a reusable `firebase_config.py` module to handle authentication and Firestore client creation.
    *   *Note*: We will need a Service Account key from the Firebase Console for the python script (Simulator) to write data securely. `firebase-tools` login is sufficient for deploying, but the Admin SDK needs credentials.

## Phase 2: The "Edge" Simulator
**Goal**: Create a robust data generator that mimics real-world industrial instruments without requiring physical hardware.
1.  **Data Schema Definition**: Define the exact JSON structure for telemetry (ID, Timestamp, Vibration, Temperature, Status).
2.  **Simulator Engine (`simulator.py`)**:
    *   Implement a class `DigitalTwinSimulator`.
    *   Logic to spawn N "Device" objects with persistent states (so they don't just randomise completely every second; they should drift or state-change logically).
    *   Write a loop that updates these states and pushes to Firestore collection `telemetry_stream`.
3.  **Command Line Interface**: Add simple flags (e.g., `--devices 10 --interval 2`) to control the simulation.

## Phase 3: The Dashboard Backbone (Streamlit)
**Goal**: Get a basic web interface running that can read and display the raw data stream.
1.  **App Skeleton (`main.py`)**: Initialize the Streamlit app with a sidebar and main container.
2.  **Data Ingestion**: Write a function to query Firestore.
    *   *Optimization*: Use Firestore `on_snapshot` or efficient polling to avoid reading the entire history every refresh.
3.  **Raw Data View**: Create a "Debug" tab in the UI to simply show the incoming JSON table, verifying the pipeline works.

## Phase 4: Operational Intelligence (OI) & Business Intelligence (BI) Visualizations
**Goal**: Translate raw data into the "Insights" promised in the customer story.
1.  **Operational Dashboard (OI)**:
    *   **Fleet Status**: A card layout showing each device with color-coded status (Green=Running, Red=Error).
    *   **Real-time Metrics**: Live line charts for Temperature/Vibration for a selected device.
2.  **Business Dashboard (BI)**:
    *   **Utilization Metric**: Calculate % of time in "Running" vs "Idle" state.
    *   **Revenue Projection**: Simple formula: `(Utilization improvements * Avg Device Revenue)`.
    *   **Comparison**: Chart showing "Before DT" vs "After DT" (simulated projection).

## Phase 5: Polish & Deployment
**Goal**: Make it demo-ready.
1.  **Styling**: Use Streamlit's configuration to verify the theme matches the "Premium/Modern" aesthetic requirements.
2.  **Readme & Docs**: Instructions on how to start the simulator in one terminal and the dashboard in another.
3.  **Final Test**: Run a full scenario: Start system -> Inject Error -> See Error on Dashboard -> Resolve Error -> See Recovery.
