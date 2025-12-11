#!/bin/bash

# Start the simulator in the background
python simulator.py &

# Start the Streamlit dashboard in the foreground
streamlit run main.py --server.port 8080 --server.address 0.0.0.0
