# FAQs Chatbot Project

## Project Overview
This project is a Frequently Asked Questions (FAQs) chatbot application designed to answer user queries. The project consists of two main components:

- **Backend**: Built using Python and Flask, it handles the chatbot logic and database management.
- **Frontend**: Provides an admin interface for managing FAQs and a user interface for interacting with the chatbot.

---

## Folder Structure
```
FAQs-chatbot-main/
├── backend/
│   ├── app.py                # Main Flask application
│   ├── db_manager.py         # Database management logic
│   ├── requirements.txt      # Backend dependencies
│   └── preload_files/
│       ├── policy.txt        # Preloaded policy file
│       └── question_answer.json  # Preloaded FAQs
│
├── frontend/
│   ├── admin/
│   │   ├── admin.html        # Admin dashboard
│   │   ├── main.js           # Admin dashboard logic
│   │   ├── package.json      # Admin dependencies
│   │   └── package-lock.json
│   │
│   └── user/
│       ├── index.html        # User chatbot interface
│       ├── main.js           # User chatbot logic
│       ├── package.json      # User dependencies
│       └── package-lock.json
```

---

## Prerequisites
Ensure you have the following installed on your system:

- **Python** (version 3.7 or above)
- **Node.js** (for managing frontend dependencies)
- **npm** (comes with Node.js)

---

## Setup Instructions

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd FAQs-chatbot-main/backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```
   The backend server will start on `http://127.0.0.1:5000/`.

### Frontend Setup
#### Admin Interface
1. Navigate to the `frontend/admin` directory:
   ```bash
   cd FAQs-chatbot-main/frontend/admin
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Open `admin.html` in a browser to access the admin dashboard.

#### User Interface
1. Navigate to the `frontend/user` directory:
   ```bash
   cd FAQs-chatbot-main/frontend/user
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Open `index.html` in a browser to access the user chatbot interface.

---

## Features
- **Admin Panel**:
  - update FAQs.
  - Manage chatbot responses.
- **User Interface**:
  - Ask questions and get responses from the chatbot.
  - Interactive and easy-to-use design.
- **Preloaded Data**:
  - Contains a sample `question_answer.json` for quick startup.

## Video Explanation

https://drive.google.com/file/d/1gWQF1SrLjuddcU74vv8ty9W9kcAMl_2t/view?usp=sharing
