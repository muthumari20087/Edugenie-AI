import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-flash-lite-latest")

def safe_generate(prompt: str) -> str:
    try:
        if not api_key:
            return
        model = genai.GenerativeModel("gemini-flash-lite-latest")
        resp = model.generate_content(prompt)
        return resp.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

app = FastAPI(title="EduGenie - Gemini Powered Learning Assistant")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class QueryRequest(BaseModel):
    question: str
    context: str = ""

class ExplainRequest(BaseModel):
    topic: str
    level: str = "beginner"

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5
    difficulty: str = "medium"

class PathRequest(BaseModel):
    goal: str
    current_level: str = "beginner"
    duration: str = "4 weeks"

class SummaryRequest(BaseModel):
    text: str
    length: str = "short"

@app.get("/api/health")
def health():
    return {"status": "ok", "model": "gemini-flash-lite-latest", "api_key_set": bool(api_key)}

@app.post("/api/ask")
def ask_question(req: QueryRequest):
    prompt = f"You are EduGenie, friendly AI assistant. Answer clearly: {req.question} Context: {req.context}"
    return {"answer": safe_generate(prompt)}

@app.post("/api/explain")
def explain_concept(req: ExplainRequest):
    prompt = f"Explain '{req.topic}' for {req.level} student with simple language, examples, key points."
    return {"explanation": safe_generate(prompt)}

@app.post("/api/quiz")
def generate_quiz(req: QuizRequest):
    prompt = f"Generate quiz on {req.topic}, {req.num_questions} Qs, {req.difficulty} level. Return ONLY valid JSON array like [{{'question':'...','options':['A','B','C','D'],'correct_answer':'B','explanation':'...'}}]"
    raw = safe_generate(prompt)
    import json, re
    try:
        m = re.search(r'\[.*\]', raw, re.DOTALL)
        data = json.loads(m.group(0) if m else raw)
        return {"quiz": data}
    except:
        return {"quiz_raw": raw}

@app.post("/api/learning-path")
def learning_path(req: PathRequest):
    prompt = f"Create learning path Goal:{req.goal} Level:{req.current_level} Duration:{req.duration} in markdown with phases, topics, resources, projects, timeline."
    return {"path": safe_generate(prompt)}

@app.post("/api/summarize")
def summarize(req: SummaryRequest):
    prompt = f"Summarize in {req.length}: {req.text}"
    return {"summary": safe_generate(prompt)}

frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")