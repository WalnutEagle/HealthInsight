# HealthInsight: RAG-Powered Medical Q&A System

The system uses a **Retrieval-Augmented Generation (RAG)** architecture to provide accurate, context-aware answers. This approach grounds the Large Language Model's (LLM) responses in factual data from the provided documents, significantly reducing the risk of hallucination. The application is served through a simple web interface built with Flask.

## Features

**Document Ingestion:** Processes text files from a `data` directory.
**Vectorization:** Uses OpenAI embeddings to convert document chunks into vectors.
**Vector Storage:** Stores and indexes vectors using FAISS for efficient similarity searches.
**QA Chain:** Utilizes Langchain and the OpenAI API (GPT-4o) to retrieve relevant documents and generate answers.
**Web Interface:** A simple Flask application provides a user-friendly chat interface.

## Setup and Usage

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
