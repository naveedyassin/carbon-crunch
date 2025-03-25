from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
from analyzers.python_analyzer import analyze_python_code
from analyzers.javascript_analyzer import analyze_javascript_code

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-code")
async def analyze_code(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        code = contents.decode("utf-8")
        filename = file.filename.lower()
        
        if filename.endswith(('.py')):
            return analyze_python_code(code)
        elif filename.endswith(('.js', '.jsx')):
            return analyze_javascript_code(code)
        else:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type. Please upload a .py, .js, or .jsx file."
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))