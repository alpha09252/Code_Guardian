import subprocess
import tempfile
import os
import re

def run_java(code: str):
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "Main.java")

        with open(src, "w") as f:
            f.write(code)

        compile_proc = subprocess.run(
            ["javac", src],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if compile_proc.returncode != 0:
            return parse_java_error(compile_proc.stderr)

        run_proc = subprocess.run(
            ["java", "-cp", tmp, "Main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if run_proc.returncode != 0:
            return {
                "success": False,
                "language": "java",
                "error_type": "RuntimeError",
                "message": run_proc.stderr
            }

        return {
            "success": True,
            "language": "java",
            "output": run_proc.stdout
        }

def parse_java_error(stderr: str):
    """
    javac error format:
    <path>/Main.java:5: error: ';' expected
        System.out.println("Hello")
    """

    line_match = re.search(r":(\d+):\s+error:\s+(.*)", stderr)

    line = int(line_match.group(1)) if line_match else None
    message = line_match.group(2).strip() if line_match else "Compilation error"

    return {
        "success": False,
        "language": "java",
        "error_type": "CompilationError",
        "line": line,
        "message": message
    }

