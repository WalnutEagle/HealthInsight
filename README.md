# HealthInsight Bot: RAG-Powered Medical Q&A System

The system uses a Retrieval-Augmented Generation (RAG) architecture to provide accurate, context-aware answers. This approach grounds the Large Language Model's (LLM) responses in factual data from the provided documents, significantly reducing the risk of hallucination. The application is served through a simple web interface built with Flask.

## Features
**Document Ingestion:** Processes text files from a `data` directory.
**Vectorization:** Uses OpenAI embeddings to convert document chunks into vectors.
**Vector Storage:** Stores and indexes vectors using FAISS for efficient similarity searches.
**QA Chain:** Utilizes Langchain and the OpenAI API (GPT-4o) to retrieve relevant documents and generate answers.
**Web Interface:** A simple Flask application provides a user-friendly chat interface.

## Local Setup and Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YourUsername/HealthInsight-Bot.git
    cd HealthInsight-Bot
    ```

2.  **Create a `.env` file** and add your OpenAI API key:
    ```
    OPENAI_API_KEY="sk-YourSecretKeyGoesHere"
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ingest your data:**
    Place your `.txt` or `.pdf` files in the `data/` directory. Then, run the ingestion script to create the vector store.
    ```bash
    python ingest.py
    ```
    This will create a `faiss_index` folder.

5.  **Run the application:**
    ```bash
    python app.py
    ```
    Open your browser and navigate to `http://127.0.0.1:5000`.

## Deployment to OpenShift

This project includes a multi-stage `Dockerfile` optimized for OpenShift. If you want to deploy it ever on Openshift then read the steps below to deploy it on Openshift and then use the external link provided for the builds to allow public access to the application. 
If you want to deploy it on a different platform change the Dockerfile as needed before deployment.

### Handling API Keys in OpenShift
This application requires the OpenAI API key both at build-time (to create the vector index) and at run-time (to answer questions). Follow these steps:

1.  **Create a Secret:** In your OpenShift project, create a new secret.
    *   **Secret Name:** `openai-secret`
    *   **Key:** `OPENAI_API_KEY`
    *   **Value:** `sk-YourSecretKeyGoesHere`

2.  **Deploy from Git:** Use the "Import from Git" feature in the Developer perspective and point it to your repository.

3.  **Configure Build-Time Secret:** Before creating the deployment, click on **"Advanced Options" -> "Build Configuration"**. Scroll down to "Build Secrets" and link your `openai-secret`. This makes the key available to the `ingest.py` script during the image build.

4.  **Configure Runtime Secret:** After the application is deployed, go to the **Deployment** configuration. In the "Environment" section, add an environment variable from a secret.
    *   Select the `openai-secret` and the `OPENAI_API_KEY` key. This will provide the key to your running application so it can answer user queries.
