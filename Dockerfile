FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Service must listen to $PORT environment variable.
# Streamlit uses 8501 by default, but Cloud Run expects 8080 usually.
# We will launch streamlit on 8080.
EXPOSE 8080

CMD streamlit run main.py --server.port 8080 --server.address 0.0.0.0
