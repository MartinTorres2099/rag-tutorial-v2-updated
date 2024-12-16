# rag-tutorial-v2
This is the extent of the README.md file from the GitHub repo. The following are my notes for the updated README.md file.

# rag-tutorial-v2-updated
The orignal README.md file from the main repo is blank. I will update this README.md file with the work I have been doing to expand on the original code.

## Description
Over a year ago I tried creating a chatbot using langchain and a vector database on my own. I was improting files, parsing them, etc. but I was having issues with the chatbot getting usefull information from the vector DB. Fast forward to a year later and now there are several repos with working implementations that you can use to chat with your documents. I forked a previous repo and was able to get it to run on my machine as it would not run from the main repo. Although this worked for small files (200KB or less), it had issues importing MB size files:

[Web-LLM-Assistant-Llama-cpp-working](https://github.com/MartinTorres2099/Web-LLM-Assistant-Llama-cpp-working/tree/main)

Before I went to deep in troubleshooting why it times out when importing large files I searched online and found this repo with code that worked the first time. It was light on features but it did what it was supposed to do:

[rag-tutorial-v2]( https://github.com/pixegami/rag-tutorial-v2.git)

With working code I set out to update it with features that I would like to see it do.

## Environment

This code is being run on a Windows 10 machine. The following will outline what you can do to recreate the environment on your machine.

From a DOS prompt, create a directory where your repo's will be stored i.e.
- CD\ 
- C:\md gitrepos
- CD C:\gitrepos
- Git clone https://github.com/MartinTorres2099/rag-tutorial-v2-updated.git

It creates the following directory:

C:\git\rag-tutorial-v2-updated

- CD C:\git\rag-tutorial-v2-updated

Create python virtual environment:

- python -m venv venv (run only once to create your vistual environment)

To activate your venv on Windows, you need to run a script that gets installed by venv. Create the virtual environment so it will not interfere with the other code you may be running for other applications:

- venv\Scripts\activate.bat

Install requirements:

(venv) C:\gitrepo\rag-tutorial-v2-updated>pip install -r requirements.txt

To deactivate virtual enviornment:

- venv\Scripts\deactivate.bat

Reboot your machine so all the paths can be updated and your environment setup properly.

Upon reboot, activate your virtual environment:

- CD C:\git\rag-tutorial-v2-updated

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

## Manually run program instead of using web interface:

Once installed and Ollama is active in your tray, run the following to pull ollam models:

(venv) C:\git\rag-tutorial-v2>ollama pull mistral (downlaoded but not used)

Specify different mistral model to pull:

(venv) C:\git\rag-tutorial-v2>ollama pull mistral-nemo (downloaded and using)

Serve the downloaded model:

(venv) C:\git\rag-tutorial-v2>ollama serve (need to verify)

To run a downloaded model:

ollama run mistral-nemo

To exit model:

/bye

To add/new documents to the database:

python populate_database.py

To test RAG answers against known information (modify the test_rag.py to test against your data):

pytest -s