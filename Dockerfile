FROM python:3.11-slim

WORKDIR /app

# copy dependency file
COPY requirements.txt .

# install deps
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

# Ensure artifacts directory exist
RUN mkdir -p /app/artifacts

RUN python app/model.py

EXPOSE 5000

CMD ["python", "run.py"]