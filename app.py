import os
import signal
import subprocess
from flask import Flask, render_template, request
from langchain_community.llms.ollama import Ollama

# Initialize Flask app
app = Flask(__name__)

# Define models categorized by their use case
CODING_MODELS = ["deepseek-coder:6.7b", "starcoder:15b", "solar", "dolphin-llama3", "nous-hermes2:10.7b", "yi-coder:9b", "codegeex4", "qwen2.5-coder:14b", "granite-code:20b", "sqlcoder:15b", "dolphin-mistral", "codegemma:7b"]
CHAT_MODELS = ["llama3-chatqa:8b", "dolphin-llama3"]
SEARCH_MODELS = ["mistral-nemo", "llama3.1:8b", "mistral", "llama3-chatqa:8b"]

# Route for the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Log the form data
        print("Form data received:", request.form)

        # Safe way to access 'user_choice'
        user_choice = request.form.get("user_choice", None)
        if not user_choice:
            return "No user choice selected", 400
        
        print(f"User choice is: {user_choice}")
        
        # Redirect or render templates with the correct user choice
        if user_choice == "search_documents":
            return render_template("search_documents.html", user_choice=user_choice, models=SEARCH_MODELS)
        elif user_choice == "coding_question":
            return render_template("coding_question.html", user_choice=user_choice, models=CODING_MODELS)
        elif user_choice == "general_chat":
            return render_template("general_chat.html", user_choice=user_choice, models=CHAT_MODELS)

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
        # Format the final command with the prompt
        print(f"Prompt being passed to Ollama: {prompt}")  # Add this for debugging
        command = f"ollama run {model_name} \"{prompt}\""
        print(f"Running command: {command}")  # Add a print to confirm the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode != 0:
            print(f"Error: {result.stderr}")  # Print stderr if the command fails
            raise Exception(f"Error running Ollama: {result.stderr}")
        return result.stdout.strip()  # Return the output from Ollama
    except Exception as e:
        print(f"Error running Ollama command: {str(e)}")
        raise Exception(f"Error running Ollama command: {str(e)}")

# Route for search_documents
@app.route("/search_documents", methods=["POST"])
def search_documents():
    # Retrieve form data (use .get() to avoid key errors)
    user_choice = request.form.get("user_choice")  # This ensures we keep track of the user choice from the previous form
    query_text = request.form.get("query_text")
    model_name = request.form.get("model_name")

    # Debugging: Print received form data
    print(f"Received user choice: {user_choice}")
    print(f"Received query: {query_text}")
    print(f"Received model: {model_name}")

    # Check if both fields are filled
    if not user_choice or not query_text or not model_name:
        return "Error: user_choice, query_text, and model_name are required.", 400

    # Generate the prompt based only on the question
    prompt_template = "{question}"  # Only the question is needed in the prompt
    prompt = prompt_template.format(question=query_text)

    # Run the Ollama command and get the model's response
    response_text = run_ollama_command(model_name, prompt)

    # If the `sources` are needed, make sure to pass them here (for simplicity, I'll set them as an empty list)
    sources = []  # If no sources are available, pass an empty list or the relevant information

    formatted_response = f"Response: {response_text}"

    return render_template("result.html", query=query_text, response_text=formatted_response, sources=sources, model=model_name)

# Route for coding question
@app.route("/coding_question", methods=["POST"])
def coding_question():
    query_text = request.form["query_text"]
    model_name = request.form["model_name"]

    prompt_template = "{question}"  # Only the question is needed in the prompt
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

    prompt_template = "{question}"  # Only the question is needed in the prompt
    prompt = prompt_template.format(question=query_text)

    # Run the Ollama command and get the model's response
    response_text = run_ollama_command(model_name, prompt)

    formatted_response = f"Response: {response_text}"

    return render_template("result.html", response_text=formatted_response)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
