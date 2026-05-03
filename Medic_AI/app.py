"""Railway entrypoint for the medical chatbot app."""

import os
import runpy
import sys


PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medical_chatbot_project")

os.chdir(PROJECT_DIR)
sys.path.insert(0, PROJECT_DIR)
runpy.run_path("app.py", run_name="__main__")
