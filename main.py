from fastapi import FastAPI
from pydantic import BaseModel
from analyzers.python_runner import run_python
from analyzers.c_runner import run_c
from analyzers.cpp_runner import run_cpp
from analyzers.java_runner import run_java
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    language: str
    code: str

@app.post("/run")
def run_code(req: CodeRequest):
    lang = req.language.lower()

    if lang == "python":
        return run_python(req.code)
    elif lang == "c":
        return run_c(req.code)
    elif lang == "cpp":
        return run_cpp(req.code)
    elif lang == "java":
        return run_java(req.code)
    else:
        return {
            "success": False,
            "error_type": "UnsupportedLanguage",
            "message": f"{lang} not supported"
        }
