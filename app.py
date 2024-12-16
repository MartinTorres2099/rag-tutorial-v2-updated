import os
import subprocess
from flask import Flask, render_template, request
from langchain.vectorstores.chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
from get_embedding_function import get_embedding_function

# Initialize Flask app
app = Flask(__name__)

CHROMA_PATH = "chroma"

# Predefined prompt templates
PROMPT_TEMPLATE_DOCS = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""

PROMPT_TEMPLATE_CHAT = """
Chat with the assistant: {question}
"""

PROMPT_TEMPLATE_CODING = """
Answer the coding question: {question}
"""

# Define models categorized by their use case
CODING_MODELS = ["deepseek-coder:6.7b", "starcoder:15b", "solar", "dolphin-llama3", "nous-hermes2:10.7b", "yi-coder:9b", "codegeex4", "qwen2.5-coder:14b", "granite-code:20b", "sqlcoder:15b", "dolphin-mistral", "codegemma:7b"]
CHAT_MODELS = ["llama3-chatqa:8b", "dolphin-llama3"]
SEARCH_MODELS = ["mistral-nemo", "llama3.1:8b", "mistral", "llama3-chatqa:8b"]

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_choice = request.form["user_choice"]
        if user_choice == "search_documents":
            return render_template("search_documents.html", models=SEARCH_MODELS)
        elif user_choice == "coding_question":
            return render_template("coding_question.html", models=CODING_MODELS)
        elif user_choice == "general_chat":
            return render_template("general_chat.html", models=CHAT_MODELS)

    return render_template("index.html")

# Function to run the Ollama command and return the model's response
def run_ollama_command(model_name, query_text):
    try:
        # Build the Ollama command
        ollama_command = f"ollama run {model_name}"

        # Run the command using subprocess and pass the query text as input
        process = subprocess.Popen(ollama_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(input=query_text.encode())

        # Check if the command was successful
        if process.returncode == 0:
            return stdout.decode()  # Return the model's response
        else:
            return f"Error: {stderr.decode()}"
    except Exception as e:
        return f"Exception: {str(e)}"

# Route for document-based queries
@app.route("/search_documents", methods=["POST"])
def search_documents():
    query_text = request.form["query_text"]
    model_name = request.form["model_name"]

    # Prepare the DB
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB
    results = db.similarity_search_with_score(query_text)

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_DOCS)
    prompt = prompt_template.format(context=context_text, question=query_text)

    # Run the Ollama command and get the model's response
    response_text = run_ollama_command(model_name, prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"

    return render_template("result.html", response_text=formatted_response)

# Route for coding question
@app.route("/coding_question", methods=["POST"])
def coding_question():
    query_text = request.form["query_text"]
    model_name = request.form["model_name"]

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_CODING)
    prompt = prompt_template.format(question=query_text)

    # Run the Ollama command and get the model's response
    response_text = run_ollama_command(model_name, prompt)

    formatted_response = f"Response: {response_text}"

    return render_template("result.html", response_text=formatted_response)

# Route for general chat
@app.route("/general_chat", methods=["POST"])
def general_chat():
    query_text = request.form["query_text"]
    model_name = request.form["model_name"]

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE_CHAT)
    prompt = prompt_template.format(question=query_text)

    # Run the Ollama command and get the model's response
    response_text = run_ollama_command(model_name, prompt)

    formatted_response = f"Response: {response_text}"

    return render_template("result.html", response_text=formatted_response)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
