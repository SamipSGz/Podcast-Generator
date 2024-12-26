# Podcast Generator

A simple web-based application to generate and download podcasts. The project consists of a frontend and backend, where the frontend handles the user interface and the backend processes audio generation requests.

# Setup and Running the Project

## Step 1: Clone the Repository

Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/podcasrgen.git
```
## Step 2: Navigate to the Backend Directory and Install Dependencies

Move to the backend directory and install dependencies:
```bash
cd backend
pip install -r requirements.txt
```
## set the Environment Variables

Ensure that the .env file in the backend directory contains any necessary configuration for the project. Example:
```bash
PLAYDIALOG_API_KEY=your_api_key
PLAYDIALOG_USER_ID=your_user_id

```

## Step 3: Run the Backend Server

Start the backend server using Uvicorn:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
The backend server will now be running at http://0.0.0.0:8000.

## Step 4: Open the Frontend

Navigate to the frontend directory and open the index.html file in your browser.
```bash
cd ../frontend
```
```bash
start index.html
(Windows)
bash
open index.html
(MacOS)
```


