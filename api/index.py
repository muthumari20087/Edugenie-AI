from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "EduGenie AI is working da! 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}
