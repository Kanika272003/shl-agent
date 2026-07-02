# SHL Assessment Recommender

A conversational AI-powered recommendation system that suggests relevant SHL assessments based on hiring requirements using natural language queries.

## Project Overview

This project was built as part of the SHL AI Internship assignment.

The system allows recruiters or hiring managers to interact with an API and receive suitable SHL assessments for specific job roles, skills, and hiring needs.

The solution supports:

- Clarifying vague user queries
- Recommending relevant SHL assessments
- Refining recommendations based on constraints
- Comparing shortlisted assessments
- Multi-turn conversational interaction

---

## Features

### 1. Clarification
If the user provides insufficient information, the system asks for:
- Job role
- Required skills
- Experience level

Example:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "I need an assessment"
    }
  ]
}
```

Response:
```json
{
  "reply": "Please tell me the job role, required skills, and experience level.",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

### 2. Recommendation
Recommends relevant SHL assessments from the SHL catalog.

Example:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Recommend SHL assessments for Python developer"
    }
  ]
}
```

---

### 3. Refinement
Supports filtering recommendations using follow-up constraints.

Example:
- Remove numerical assessments
- Show only personality tests

---

### 4. Comparison
Compares shortlisted assessments and returns comparison insights.

Example:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Recommend SHL assessments for Python developer"
    },
    {
      "role": "user",
      "content": "Compare recommended assessments"
    }
  ]
}
```

---

# Architecture

The system is built using modular FastAPI architecture.

Components:

- **FastAPI API Service**
- **Intent Detection Module**
- **Guardrail Module**
- **Recommendation Engine**
- **Refinement Engine**
- **Comparison Engine**
- **Gemini LLM Response Generator**

Flow:

User Query  
→ Guardrails  
→ Intent Detection  
→ Recommendation / Refine / Compare  
→ LLM Response Generation  
→ JSON Response

---

# Retrieval Strategy

The SHL-provided catalog JSON is used as the retrieval source.

Each assessment contains:
- Assessment name
- Product URL
- Test category
- Description metadata

Retrieval uses weighted keyword scoring:

- Name match weight = 5
- Category match weight = 3
- Description match weight = 1
- Phrase bonus for exact matches

Preprocessing:
- Lowercasing
- Stopword removal
- Synonym normalization

Example synonym mapping:
- engineer → developer
- aptitude → cognitive
- judgment → situational

---

# Tech Stack

- Python 3
- FastAPI
- Pydantic
- Uvicorn
- Google Gemini 1.5 Flash
- Render (Deployment)

---

# API Endpoints

## Root Endpoint

GET `/`

Response:
```json
{
  "message": "SHL Assessment Recommender API is running"
}
```

---

## Health Check

GET `/health`

Response:
```json
{
  "status": "ok"
}
```

---

## Chat Endpoint

POST `/chat`

Request Body:
```json
{
  "messages": [
    {
      "role": "user",
      "content": "Recommend SHL assessments for Python developer"
    }
  ]
}
```

Response Format:
```json
{
  "reply": "string",
  "recommendations": [],
  "end_of_conversation": false
}
```

---

# Deployment

Public API Base URL:

https://shl-agent-ox0s.onrender.com

Swagger Documentation:

https://shl-agent-ox0s.onrender.com/docs

---

# Local Setup

Clone repository:

```bash
git clone https://github.com/Kanika272003/shl-agent.git
cd shl-agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set environment variable:

```env
GOOGLE_API_KEY=your_api_key
```

Run locally:

```bash
uvicorn app.main:app --reload
```

---

# Limitations

Current limitations:

- Keyword-based retrieval may miss semantic similarity
- No vector database / embeddings yet
- Render free tier causes cold start delay

Future improvements:
- Semantic search using embeddings
- Better ranking with reranking models
- Session memory support

---

# AI Assistance Disclosure

AI tools used during development:

- ChatGPT
- Claude
- Google Gemini

These tools assisted with debugging, architecture discussions, refactoring, and documentation support.

---

# Author

**Kanika Tomar**  
B.Tech CSE (Data Science)  
SHL AI Internship Assignment