import time
import random
import datetime
from faker import Faker
from firebase_config import db  # Import the Firestore client

fake = Faker()

# Configuration
NUM_DEVICES = 5
UPDATE_INTERVAL_SEC = 3.0

class AnalyticalInstrument:
    def __init__(self, device_id):
        self.device_id = device_id
        self.model = random.choice(["Spectro-X200", "Chroma-9000", "AnalyzePro-V1"])
        self.location = f"Lab-{random.randint(1, 5)}"
        self.commission_date = fake.date_between(start_date='-3y', end_date='today').isoformat()
        
        # Operational State
        self.status = "IDLE"  # IDLE, RUNNING, ERROR, MAINTENANCE
        self.temperature = 25.0
        self.vibration = 0.01
        self.throughput = 0
        self.error_code = None
        self.operator_id = None
        
        # Simulation drift factors
        self._temp_target = 25.0
        
    def tick(self):
        """Advance time by one step for this device."""
        
        # 1. State Transitions
        if self.status == "IDLE":
            if random.random() < 0.1:
                self.start_run()
        elif self.status == "RUNNING":
            if random.random() < 0.05:
                self.finish_run()
            elif random.random() < 0.02:
                self.trigger_error()
        elif self.status == "ERROR":
            if random.random() < 0.2:
                self.resolve_error()

        # 2. Metric Simulation
        if self.status == "RUNNING":
            self._temp_target = 60.0 + random.uniform(-5, 5)
            self.vibration = random.uniform(0.1, 0.4)
            self.throughput = random.randint(10, 20)
        elif self.status == "ERROR":
            self.vibration = random.uniform(0.5, 1.2) # Spiking vibration
            self.throughput = 0
        else:
            self._temp_target = 22.0
            self.vibration = 0.01
            self.throughput = 0

        # Smooth temperature changes
        self.temperature += (self._temp_target - self.temperature) * 0.1
        
    def start_run(self):
        self.status = "RUNNING"
        self.operator_id = f"OP-{random.randint(10, 99)}"
        self.error_code = None
        print(f"[{self.device_id}] Started run by {self.operator_id}")

    def finish_run(self):
        self.status = "IDLE"
        self.operator_id = None
        print(f"[{self.device_id}] Finished run")

    def trigger_error(self):
        self.status = "ERROR"
        self.error_code = random.choice(["ERR_OVERHEAT", "ERR_CALIBRATION", "ERR_SENSOR_FAIL"])
        print(f"[{self.device_id}] CRITICAL ERROR: {self.error_code}")

    def resolve_error(self):
        self.status = "IDLE"
        self.error_code = None
        print(f"[{self.device_id}] Error resolved")

    def get_telemetry(self):
        """Return the current metrics as a dict."""
        return {
            "device_id": self.device_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": self.status,
            "metrics": {
                "temperature": round(self.temperature, 2),
                "vibration": round(self.vibration, 4),
                "throughput": self.throughput
            },
            "meta": {
                "operator": self.operator_id,
                "error_code": self.error_code,
                "model": self.model,
                "location": self.location
            }
        }

def main():
    print("--- Starting Operational Digital Twin Simulator ---")
    
    if db is None:
        print("x Firebase not connected. Running in dry-run mode (printing only).")
    else:
        print("Firebase connected. Streaming data to Firestore...")

    # Initialize Fleet
    fleet = [AnalyticalInstrument(f"INST-{i:03d}") for i in range(1, NUM_DEVICES + 1)]
    
    # Register Devices (Static Metadata) - Optional, but good for the 'Registry' view
    if db:
        print("Registering devices...")
        batch = db.batch()
        for dev in fleet:
            doc_ref = db.collection("device_registry").document(dev.device_id)
            batch.set(doc_ref, {
                "model": dev.model,
                "location": dev.location,
                "commission_date": dev.commission_date
            })
        try:
            batch.commit()
            print("Registry updated.")
        except Exception as e:
            print(f"Registry update failed: {e}")

    # Main Data Loop
    try:
        while True:
            for dev in fleet:
                dev.tick()
                data = dev.get_telemetry()
                
                # Print local status
                status_icon = "[RUN]" if dev.status == "RUNNING" else ("[ERR]" if dev.status == "ERROR" else "[IDLE]")
                print(f"{status_icon} {dev.device_id}: {dev.status} | T:{data['metrics']['temperature']}C")

                # Push to Cloud
                if db:
                    # We store in a time-series collection. 
                    # Note: For High HF data we'd use TimeScale or similar, but Firestore is fine for this demo.
                    db.collection("telemetry_stream").add(data)
                    
                    # Update 'latest' state in registry for easier realtime view
                    db.collection("device_registry").document(dev.device_id).update({
                        "last_seen": data["timestamp"],
                        "current_status": data["status"],
                        "latest_metrics": data["metrics"]
                    })
            
            time.sleep(UPDATE_INTERVAL_SEC)
            print("-" * 20)

    except KeyboardInterrupt:
        print("\nStopping simulator.")

if __name__ == "__main__":
    main()
