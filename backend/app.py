from flask import request, jsonify
from __init__ import create_app, db
from db_manager import UploadedFiles,ChatRecord  
import os
import json
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage,SystemMessage


load_dotenv()
app = create_app()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route('/ask', methods=['POST'])
def chat():
    data = request.get_json()  
    user_id = data.get("user_id", "default_user")
    user_message = data.get("message", "").lower()

    if not user_message:
        return jsonify({"response": "Please provide a message."})

    # Load vector store and search for relevant documents
    embedder = GoogleGenerativeAIEmbeddings(model='models/embedding-001', google_api_key=GEMINI_API_KEY)
    knowledge_base = FAISS.load_local("knowledge_base", embeddings=embedder, allow_dangerous_deserialization=True)
    relevant_docs = knowledge_base.similarity_search(query=user_message, k=2)

    # Combine context from top-k similar documents
    combined_context = ''.join([doc.page_content for doc in relevant_docs])

    # Fallback response if no relevant documents are found
    if not combined_context.strip():
        fallback_response = (
            "I couldn't find relevant information to answer your question. "
        )
        return jsonify({"response": fallback_response})

    
    system_prompt = (
        "You are a helpful assistant. Use the provided context to answer the user's question accurately. "
        "If the context doesn't contain the information needed, respond politely saying  I couldn't find relevant information to answer your question. "
        f"Context:\n{combined_context}"
    )

    llm = ChatGoogleGenerativeAI(model='models/gemini-1.5-flash', api_key=GEMINI_API_KEY)
    prompt = [
        SystemMessage(system_prompt),
        HumanMessage(user_message)
    ]
    response = llm.invoke(prompt)
    bot_reply = response.content

    # Save chat interaction to database
    chat_record = ChatRecord(user_id=user_id, query=user_message, response=bot_reply)
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

    # update the vectore database
    text_splitter = RecursiveCharacterTextSplitter()
    docs = text_splitter.split_text(str(file_content))
    embedder = GoogleGenerativeAIEmbeddings(
        model='models/embedding-001',
        google_api_key=GEMINI_API_KEY
    )
    knowledge_db = FAISS.load_local("knowledge_base",embeddings=embedder,allow_dangerous_deserialization=True)
    knowledge_db.add_documents(docs)
    knowledge_db.save_local("knowledge_base")
    return jsonify({"message": f"File '{file.filename}' uploaded and content saved to database!"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the database tables are created
    app.run(port=5000)
