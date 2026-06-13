import subprocess
import tempfile
import os
import re

def run_c(code: str):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "main.c")
        exe = os.path.join(tmp, "main")

        with open(src, "w") as f:
            f.write(code)

        compile_proc = subprocess.run(
            ["gcc", src, "-o", exe],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if compile_proc.returncode != 0:
            return parse_gcc_error(compile_proc.stderr, "c")

        run_proc = subprocess.run(
            [exe],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if run_proc.returncode != 0:
            return {
                "success": False,
                "language": "c",
                "error_type": "RuntimeError",
                "message": run_proc.stderr
            }

        return {
            "success": True,
            "language": "c",
            "output": run_proc.stdout
        }

def parse_gcc_error(stderr: str, language: str):
  

    match = re.search(r":(\d+):\d+:\s+error:\s+(.*)", stderr)

    line = int(match.group(1)) if match else None
    message = match.group(2).strip() if match else "Compilation error"

    return {
        "success": False,
        "language": language,
        "error_type": "CompilationError",
        "line": line,
        "message": message
    }
