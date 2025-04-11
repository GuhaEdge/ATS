from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from resume_parser_logic import process_resume

app = FastAPI()

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    content = await file.read()
    result = process_resume(content)
    return JSONResponse(content=result)