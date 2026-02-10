![Aditi Icon](https://github.com/Nikdroid-sys/Conversational-AI-Portfolio/blob/main/frontend/public/aditi.svg) 

# AI Portfolio Chatbot

A conversational AI designed to provide a dynamic and interactive way to explore Nikhil Chaube's professional portfolio. Ask it anything about his resume, skills, or projects!

## About the Persona: Aditi

The chatbot is embodied by **Aditi**, a persona inspired by ancient wisdom and history. Aditi's role is to guide you through Nikhil's professional journey with a calm, clear, and gentle storytelling approach.

## Core Features

-   **Conversational Resume**: Engage in a natural conversation about professional experience.
-   **RAG-Powered**: Uses a Retrieval-Augmented Generation (RAG) pipeline to provide answers based on resume data.
-   **Streaming Responses**: Answers are streamed in real-time for a more dynamic user experience.
-   **Multi-LLM Support**: Easily switch between LLM providers like Gemini, OpenAI, or a local Ollama instance.
-   **Sleek, Responsive UI**: A minimalist, glassmorphism-style interface that looks great on any device.

## Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

-   **Python 3.10+**
-   **Node.js v18+**
-   **Git**

### 1. Clone the Repository

```bash
git clone https://github.com/Nikdroid-sys/Conversational-AI-Portfolio.git
cd Conversational-AI-Portfolio
```

### 2. Set Up the Backend

The backend powers the AI and chat logic.

```bash
# Navigate to the backend directory
cd backend

# Install required Python packages
pip install -r requirements.txt

# Ingest the data (run this once initially)
python app/core/ingestion.py
```

### 3. Set Up the Frontend

The frontend is the user interface you interact with.

```bash
# Navigate to the frontend directory from the root
cd frontend

# Install required Node.js packages
npm install
```

### 4. Configure API Keys

-   Create a file named `.env` in the root of the project (`ai-chatbot/`).
-   Add your API keys to this file. At a minimum, you'll need one for your chosen LLM provider.

```env
# Example for Google Gemini
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
MODEL_PROVIDER="gemini"
```

## Usage

To run the application, you need to start both the backend and frontend servers in separate terminals.

1.  **Start the Backend Server**
    -   Terminal 1: Navigate to the `backend` directory.
    -   Run: `uvicorn app.main:app --reload`
    -   The backend will be running at `http://localhost:8000`.

2.  **Start the Frontend Server**
    -   Terminal 2: Navigate to the `frontend` directory.
    -   Run: `npm run dev`
    -   The frontend will be running at `http://localhost:5173` (or another port if 5173 is busy).

You can now open your browser to the frontend URL and start chatting!

## Tech Stack

-   **Backend**: Python, FastAPI, LangChain, Sentence-Transformers, FAISS
-   **Frontend**: React, Vite, CSS
-   **LLMs**: Gemini, OpenAI, Ollama (configurable)