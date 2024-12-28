```markdown
# rag-tutorial-v2 - Updated

This repository expands on the original [rag-tutorial-v2](https://github.com/pixegami/rag-tutorial-v2.git) to add more features and improve the performance of the chatbot built with Langchain and a vector database. Below is a guide to set up the environment and run the application.

---

## Description

Over a year ago, I attempted to create a chatbot using Langchain and a vector database. Although I could import files and parse them, I faced challenges getting useful information from the vector DB. Fast forward to today, and many repositories offer working implementations for chatting with documents.

I initially forked and tested a repo ([Web-LLM-Assistant-Llama-cpp-working](https://github.com/MartinTorres2099/Web-LLM-Assistant-Llama-cpp-working/tree/main)) but faced issues with importing larger files (greater than 200KB). After troubleshooting, I found [rag-tutorial-v2](https://github.com/pixegami/rag-tutorial-v2.git), which worked well for smaller documents and served as a base for my updates.

I expanded the project with additional features that I wanted to see. Here's a [video demo of the app in action](https://www.youtube.com/watch?v=2TJxpyO3ei4).

---

## Environment Setup

This project is set up to run on a Windows 10 machine. Follow the instructions below to recreate the environment on your machine.

### 1. Clone the Repository

First, create a directory to store your repositories and clone the project.

```bash
# Navigate to the root directory where your repos will be stored
cd \
mkdir gitrepos
cd gitrepos

# Clone the repository
git clone https://github.com/MartinTorres2099/rag-tutorial-v2-updated.git
```

The repository will be cloned to:  
`C:\gitrepos\rag-tutorial-v2-updated`

### 2. Set Up the Python Virtual Environment

Navigate to the project directory and create a Python virtual environment:

```bash
cd C:\gitrepos\rag-tutorial-v2-updated
python -m venv venv  # Run only once to create your virtual environment
```

### 3. Activate the Virtual Environment

To activate the virtual environment on Windows:

```bash
venv\Scripts\activate.bat
```

### 4. Install the Required Packages

Install the required dependencies by running:

```bash
pip install -r requirements.txt
```

Additionally, install Flask and Langchain:

```bash
pip install Flask
pip install langchain-community
```

### 5. Deactivate the Virtual Environment

Once you are done working, deactivate the virtual environment with:

```bash
venv\Scripts\deactivate.bat
```

---

## Modifying the Embedding Function

Update `get_embedding_function.py` to run locally by uncommenting and adjusting the code:

```python
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings

def get_embedding_function():
    # Uncomment and configure to use cloud-based embeddings
    # embeddings = BedrockEmbeddings(credentials_profile_name="default", region_name="us-east-1")
    
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings
```

---

## Loading Documents

You can load different document types using Langchain's document loaders. Find more details here:

- [General document loaders](https://python.langchain.com/docs/how_to/#document-loaders)
- [Loading PDF files](https://python.langchain.com/docs/how_to/document_loader_pdf/)

To install Ollama, follow the instructions on their [official website](https://ollama.com/).

---

## Running the Application

### Prerequisites

Ensure that the **Ollama** application is running on your machine before starting the app. You can create a batch file to automate the process.

### 1. Create a Batch File to Launch the Application

Create a batch file (`start_app.bat`) with the following content:

```batch
@echo off
echo This will launch the RAG application
timeout /t 2

echo Changing to rag directory
cd C:\rag-tutorial-v2
timeout /t 2

echo Activating Python virtual environment
call venv\Scripts\activate.bat
timeout /t 2

python app.py
echo Waiting for the app to close...
timeout /t 2

echo Deactivating Python virtual environment
call venv\Scripts\deactivate.bat
timeout /t 2

echo Thank you for using the RAG application, goodbye for now!
timeout /t 2

exit
```

### 2. Run the Web App

Execute the batch file to start the application. The app will run a local development server, accessible at:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## Running the Program Without the Web Interface

You can also run the program manually without the web interface:

1. **Pull the Nomic embed model:**

```bash
ollama pull nomic-embed-text
```

2. **Download and use a Mistral model:**

```bash
ollama pull mistral-nemo  # Pull the Mistral model
```

3. **Serve the model:**

```bash
ollama serve  # (Verify if needed)
```

4. **Run the model:**

```bash
ollama run mistral-nemo
```

5. **Exit the model:**

```bash
/bye
```

6. **Add or update documents in the database:**

```bash
python populate_database.py
```

7. **Test the RAG system with known data:**

Run the following to check how well the LLM answers questions based on the vector DB:

```bash
pytest -s  # Modify test_rag.py with known data
```

---

## Uninstalling the Python Virtual Environment

To uninstall the virtual environment, first deactivate it:

```bash
venv\Scripts\deactivate.bat
```

Then, delete the virtual environment:

```bash
rm -r venv
```

---

## Additional Resources

- [Langchain Documentation](https://python.langchain.com/docs/)
- [Ollama Website](https://ollama.com/)

---

Thank you for using this project! Feel free to contribute or make improvements.

```

---

