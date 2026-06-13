import tempfile
import subprocess
import traceback
import sys

def run_python(code: str):
    try:
        compile(code, "<user_code>", "exec")
    except SyntaxError as e:
        return {
            "success": False,
            "language": "python",
            "error_type": "SyntaxError",
            "line": e.lineno,
            "message": e.msg
        }

    try:
        exec(code, {})
        return {
            "success": True,
            "language": "python",
            "output": "Program executed successfully"
        }
    except Exception as e:
        tb = traceback.extract_tb(sys.exc_info()[2])
        last = tb[-1]
        return {
            "success": False,
            "language": "python",
            "error_type": type(e).__name__,
            "line": last.lineno,
            "message": str(e)
        }
