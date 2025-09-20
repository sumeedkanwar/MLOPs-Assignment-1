# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# copy dependency file
COPY requirements.txt .

# install deps
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# Ensure artifacts directory exists
RUN mkdir -p /app/artifacts

# Train model during image build (optional but convenient)
# This step can be heavy; if you prefer, comment it out and pre-build the model locally.
RUN python app/model.py

EXPOSE 5000

CMD ["python", "run.py"]
