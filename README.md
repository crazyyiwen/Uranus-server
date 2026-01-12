# Uranus Server

A FastAPI-based AI agent server with LangChain, LangGraph, and multi-provider LLM support.

## Features

- FastAPI web framework
- LangChain & LangGraph for AI workflows
- Multi-provider LLM support (OpenAI, Anthropic, Google)
- Tavily search integration
- MCP (Model Context Protocol) adapters
- DeepAgents integration

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# Copy the example env file
copy .env.example .env

# Edit .env and add your API keys
```

## Running the Server

### Development Mode (with auto-reload):
```bash
uvicorn main:app --reload
```

Or simply:
```bash
python main.py
```

### Production Mode:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Root endpoint, returns welcome message
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Default Configuration

- Host: `0.0.0.0`
- Port: `8000`
- Auto-reload: Enabled in development mode
