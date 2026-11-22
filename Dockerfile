FROM apache/airflow:3.1.4-python3.12

COPY requirements.txt /tmp/requirements.txt
RUN python -m venv /opt/airflow/pipeline-venv \
 && /opt/airflow/pipeline-venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt