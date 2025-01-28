from flask import request, jsonify
from __init__ import create_app, db
from db_manager import UploadedFiles,ChatRecord  
import os
import json
from dotenv import load_dotenv
import requests
from PyPDF2 import PdfReader


load_dotenv()
app = create_app()
HF_API_KEY=os.getenv("HF_API_KEY")

INFERENCE_API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

headers = {
    "Authorization": f"Bearer {HF_API_KEY}"
}

@app.route('/ask', methods=['POST'])
def chat():
    data = request.get_json()  # Get user message
    user_message = data.get("message", "").lower()

    if not user_message:
        return jsonify({"response": "Please provide a message."})

    # Fetch all content from the UploadedFiles table
    uploaded_files = UploadedFiles.query.all()
    combined_context = " ".join(file.file_content for file in uploaded_files)  # Combine all file content

    if not combined_context:
        return jsonify({"response": "No context available to answer your question."})

    # Prepare the payload for the Hugging Face API
    payload = {
        "inputs": {
            "question": user_message,
            "context": combined_context
        }
    }

    response = requests.post(INFERENCE_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        # Check if the API returned an answer
        bot_reply = response_data.get("answer", "I'm sorry, I couldn't find an answer to your question.")
        if not bot_reply.strip():  # Fallback response if the answer is empty
            bot_reply = "I'm sorry, I couldn't find an answer to your question. Please check the company's policies or FAQs, or reach out to support."
    else:
        bot_reply = "An error occurred while processing your request. Please try again later."

    # Store the query and response in the database
    chat_record = ChatRecord(
        user_id="default_user",  
        query=user_message,
        response=bot_reply
    )
    db.session.add(chat_record)
    db.session.commit()

    return jsonify({"response": bot_reply})

@app.route('/admin/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    # Save file to the file system
    file_path = os.path.join("preload_files", file.filename)
    os.makedirs("preload_files", exist_ok=True)  # Ensure the directory exists
    file.save(file_path)

    # Determine file type based on extension
    file_extension = file.filename.split('.')[-1].lower()

    try:
        # Reopen the file to read its content
        if file_extension == 'pdf':
            # Parse the PDF and extract text
            file_content = ""
            with open(file_path, 'rb') as saved_file:
                reader = PdfReader(saved_file)
                for page in reader.pages:
                    file_content += page.extract_text()
                print(file_content)
        elif file_extension == 'json':
            # If the file is JSON, load the content as JSON
            with open(file_path, 'r', encoding='utf-8') as saved_file:
                try:
                    file_content = json.load(saved_file)
                    file_content = json.dumps(file_content)  # Convert back to string to store in DB
                except json.JSONDecodeError:
                    return jsonify({"message": "Invalid JSON file"}), 400
        elif file_extension in {'md', 'txt'}:
            # If the file is Markdown or plain text, read as plain text
            with open(file_path, 'r', encoding='utf-8') as saved_file:
                file_content = saved_file.read()
        else:
            return jsonify({"message": "Unsupported file type"}), 400
    except Exception as e:
        return jsonify({"message": f"Error reading file: {str(e)}"}), 500

    # Store file metadata and content in the database
    uploaded_file = UploadedFiles(filename=file.filename, file_content=file_content)
    db.session.add(uploaded_file)
    db.session.commit()

    return jsonify({"message": f"File '{file.filename}' uploaded and content saved to database!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    app.run(port=5000)
