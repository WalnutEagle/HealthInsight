FROM python:3.10-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./data ./data
COPY ingest.py .

# IMPORTANT: You must provide the OpenAI API Key as a build secret in OpenShift
# or as a build argument locally like: docker build --build-arg OPENAI_API_KEY="sk-..."
# This Dockerfile expects the key to be available during the build.
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

RUN python ingest.py

FROM python:3.10-slim

WORKDIR /app
RUN groupadd -r appgroup && useradd --no-log-init -r -g appgroup appuser
COPY app.py .
COPY templates ./templates
COPY --from=builder /app/faiss_index ./faiss_index

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
