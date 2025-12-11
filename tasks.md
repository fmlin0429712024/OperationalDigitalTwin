# Project Tasks

## Phase 1: Environment
- [x] **[1.1]** Initialize Python Virtual Environment (`venv`) <!-- id: 1.1 -->
- [x] **[1.2]** Create `requirements.txt` and install dependencies (`streamlit`, `firebase-admin`, `plotly`, `pandas`, `faker`) <!-- id: 1.2 -->
- [ ] **[1.3]** Generate Firebase Service Account Key (User action required: Download from Console) and save as `serviceAccountKey.json` <!-- id: 1.3 -->
- [x] **[1.4]** Create `firebase_config.py` to initialize Admin SDK <!-- id: 1.4 -->

## Phase 2: Simulator
- [x] **[2.1]** Create `simulator.py` skeleton <!-- id: 2.1 -->
- [x] **[2.2]** Implement `Device` class with state logic (Running -> Idle -> Error transitions) <!-- id: 2.2 -->
- [x] **[2.3]** Implement Firestore write logic in the simulator loop <!-- id: 2.3 -->
- [ ] **[2.4]** Test simulator: Verify data is appearing in Firebase Console <!-- id: 2.4 -->

## Phase 3: Basic Dashboard
- [x] **[3.1]** Create `main.py` with Streamlit text header <!-- id: 3.1 -->
- [x] **[3.2]** Implement Firestore read logic (fetch latest N records) <!-- id: 3.2 -->
- [x] **[3.3]** Create a "Raw Data" dataframe display to verify connection <!-- id: 3.3 -->
- [x] **[3.4]** Implement Auto-Refresh mechanism (loops or `st.empty` container updates) <!-- id: 3.4 -->

## Phase 4: Analytic Features
- [x] **[4.1]** UI: Create "Fleet Overview" cards (Metric components) <!-- id: 4.1 -->
- [x] **[4.2]** UI: Create "Real-time Charts" using Plotly (Temperature/Vibration) <!-- id: 4.2 -->
- [x] **[4.3]** Logic: Calculate System Utilization % from data history <!-- id: 4.3 -->
- [x] **[4.4]** UI: Create "Business Impact" section (Revenue/Savings Calculator) <!-- id: 4.4 -->

## Phase 5: Polish
- [x] **[5.1]** Apply specific Streamlit theme (colors, wide mode) <!-- id: 5.1 -->
- [x] **[5.2]** Create `README.md` with "How to Run" instructions <!-- id: 5.2 -->
- [x] **[5.3]** Final walkthrough and code cleanup <!-- id: 5.3 -->
