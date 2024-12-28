# rag-tutorial-v2
This is the extent of the README.md file from the GitHub repo. The following are my notes for the updated README.md file.

# rag-tutorial-v2-updated
The orignal README.md file from the main repo is blank. I will update this README.md file with the work I have been doing to expand on the original code.

## Description
Over a year ago I tried creating a chatbot using langchain and a vector database on my own. I was importing files, parsing them, etc. but I was having issues with the chatbot getting usefull information from the vector DB. Fast forward to a year later and now there are several repos with working implementations that you can use to chat with your documents. I forked a previous repo and was able to get it to run on my machine as it would not run from the main repo. Although this worked for small files (200KB or less), it had issues importing MB size files:

[Web-LLM-Assistant-Llama-cpp-working](https://github.com/MartinTorres2099/Web-LLM-Assistant-Llama-cpp-working/tree/main)

Before I went to deep in troubleshooting why it times out when importing large files I searched online and found this repo with code that worked the first time. It was light on features but it did what it was supposed to do:

[rag-tutorial-v2]( https://github.com/pixegami/rag-tutorial-v2.git)

With working code I set out to update it with features that I would like to see it do.

[Youtube video showing the application working]( https://www.youtube.com/watch?v=2TJxpyO3ei4 )

## Environment

This code is being run on a Windows 10 machine. The following will outline what you can do to recreate the environment on your machine.

From a DOS prompt, create a directory where your repo's will be stored i.e.
- CD\ 
- C:\md gitrepos
- CD C:\gitrepos
- Git clone https://github.com/MartinTorres2099/rag-tutorial-v2-updated.git

It creates the following directory:

C:\gitrepo\rag-tutorial-v2-updated

- CD C:\gitrepo\rag-tutorial-v2-updated

Create python virtual environment:

- python -m venv venv (run only once to create your vistual environment)

To activate your venv on Windows, you need to run a script that gets installed by venv. Create the virtual environment so it will not interfere with the other code you may be running for other applications:

- venv\Scripts\activate.bat

Install requirements:

(venv) C:\gitrepo\rag-tutorial-v2-updated>pip install -r requirements.txt

- Install Flask: If you don't have Flask installed, you can install it via pip:
  pip install Flask

- pip install langchain-community


To deactivate virtual enviornment:

- venv\Scripts\deactivate.bat

Reboot your machine so all the paths can be updated and your environment setup properly.

Upon reboot, activate your virtual environment:

- CD C:\gitrepo\rag-tutorial-v2-updated

- venv\Scripts\activate.bat

Modify get_embedding_function.py to run locally:
```
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings

def get_embedding_function():
    # Code is commented out - uncomment and update to use embeddings from cloud provider
    # embeddings = BedrockEmbeddings(
    #     credentials_profile_name="default", region_name="us-east-1"
    # )
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    return embeddings

```


To load different document types, look for code here:

https://python.langchain.com/docs/how_to/#document-loaders

To load PDF files, look for code here:

https://python.langchain.com/docs/how_to/document_loader_pdf/

To install Ollama, look for code here:

https://ollama.com/

## Running the app from the website

Make sure you start the Ollama application on your machine before starting the app. I created a batch file to launch my application. You can modify it to suite your environment:

```
@echo off
echo This will launch the RAG application
timeout /t 2

echo Chagning to rag directory
cd C:\rag-tutorial-v2
timeout /t 2

echo Activating python virtual environment
call venv\Scripts\activate.bat
timeout /t 2

python app.py
echo Waiting for the app to close...
timeout /t 2

echo Deactivating python virtual environment
call venv\Scripts\deactivate.bat
timeout /t 2

echo Thank you for using the RAG application, goodbye for now!
timeout /t 2

exit
```

Running the Web App:
- To start the Flask app, simply run the Python script (python your_script.py).

It will start a local development server, which can be accessed by navigating to http://127.0.0.1:5000/ in a web browser.

## Manually run program instead of using web interface:

Make sure to pull the nomic-embed-text into the environment:

ollama pull nomic-embed-text

Once installed and Ollama is active in your tray, run the following to pull ollam models:

(venv) C:\gitrepo\rag-tutorial-v2>ollama pull mistral (downlaoded but not used)

Specify different mistral model to pull:

(venv) C:\gitrepo\rag-tutorial-v2>ollama pull mistral-nemo (downloaded and using)

Serve the downloaded model:

(venv) C:\gitrepo\rag-tutorial-v2>ollama serve (need to verify)

To run a downloaded model:

ollama run mistral-nemo

To exit model:

/bye

To add/new documents to the database:

python populate_database.py

To test RAG answers against known information (modify the test_rag.py to test against your data):

pytest -s

pytest will check the code in test_rag.py. You need to update this file with information you know to be true.
This way you can check how well your LLM is answering your questions based on the information stored in the vector DB.

## Uninstall Python Virtual Environment

From a powershell CMD prompt, make sure your virutal environment is not active:

- venv\Scripts\deactivate.bat

Run the following Powershell command to remove the python virutal environment:

- rm -r venv