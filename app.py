import os
import signal
import subprocess
import secrets
from flask import Flask, render_template, request, session, redirect
from langchain_community.llms.ollama import Ollama

# Initialize Flask app
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Define models categorized by their use case
CODING_MODELS = ["deepseek-coder:6.7b", "starcoder:15b", "solar", "dolphin-llama3", "nous-hermes2:10.7b", "yi-coder:9b", "codegeex4", "qwen2.5-coder:14b", "granite-code:20b", "sqlcoder:15b", "dolphin-mistral", "codegemma:7b"]
CHAT_MODELS = ["llama3-chatqa:8b", "dolphin-llama3"]
SEARCH_MODELS = ["mistral-nemo", "llama3.1:8b", "mistral", "llama3-chatqa:8b"]

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    # Clear any existing model selection when returning to index
    session.pop('selected_model', None)
    session.pop('question_type', None)

    if request.method == "POST":
        question_type = request.form.get("user_choice")
        if not question_type:
            return "No user choice selected", 400
        
        session['question_type'] = question_type
        
        if question_type == "search_documents":
            return render_template("search_documents.html", models=SEARCH_MODELS)
        elif question_type == "coding_question":
            return render_template("coding_question.html", models=CODING_MODELS)
        elif question_type == "general_chat":
            return render_template("general_chat.html", models=CHAT_MODELS)

    return render_template("index.html")

@app.route('/quit', methods=["POST"])
def quit_app():
    """Shut down the Flask server gracefully."""
    # Send the SIGINT signal to the current process to shut it down
    os.kill(os.getpid(), signal.SIGINT)
    return 'Shutting down...'

# Function to run the Ollama command and return the model's response
def run_ollama_command(model_name, prompt):
    try:
        command = f"ollama run {model_name} \"{prompt}\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            raise Exception(f"Error running Ollama: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        raise Exception(f"Error running Ollama command: {str(e)}")

@app.route("/process_question", methods=["POST"])
def process_question():
    query_text = request.form.get("query_text")
    
    # Get model from session or form
    model_name = session.get('selected_model')
    if not model_name:
        model_name = request.form.get("model_name")
        session['selected_model'] = model_name
    
    response_text = run_ollama_command(model_name, query_text)
    formatted_response = f"Response: {response_text}"
    
    return render_template(
        "result.html",
        query=query_text,
        response_text=formatted_response,
        sources=[],
        model=model_name
    )

@app.route("/ask_another", methods=["GET"])
def ask_another():
    model_name = session.get('selected_model')
    if not model_name:
        return redirect('/')
    return render_template("ask_question.html", model=model_name)

@app.route("/ask_question", methods=["POST"])
def ask_question():
    query_text = request.form.get("query_text")
    model_name = session.get('selected_model')
    
    if not query_text or not model_name:
        return redirect('/')
        
    response_text = run_ollama_command(model_name, query_text)
    return render_template("result.html", query=query_text, response_text=response_text, sources=[], model=model_name)

# Route for search_documents
@app.route("/search_documents", methods=["POST"])
def search_documents():
    query_text = request.form.get("query_text")
    model_name = request.form.get("model_name")
    session['selected_model'] = model_name  # Store model in session
    
    response_text = run_ollama_command(model_name, query_text)
    
    return render_template("result.html", 
                         query=query_text,
                         response_text=response_text,
                         sources=[],
                         model=model_name)

# Route for coding question
@app.route("/coding_question", methods=["POST"])
def coding_question():
    query_text = request.form.get("query_text")
    model_name = request.form.get("model_name")
    session['selected_model'] = model_name
    
    response_text = run_ollama_command(model_name, query_text)
    
    return render_template("result.html",
                         query=query_text, 
                         response_text=response_text,
                         sources=[],
                         model=model_name)

# Route for general chat
@app.route("/general_chat", methods=["POST"])
def general_chat():
    query_text = request.form.get("query_text")
    model_name = request.form.get("model_name")
    session['selected_model'] = model_name
    
    response_text = run_ollama_command(model_name, query_text)
    
    return render_template("result.html",
                         query=query_text,
                         response_text=response_text,
                         sources=[],
                         model=model_name)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
