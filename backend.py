pip install fastapi uvicorn gitpython

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import git
import os
import subprocess

app = FastAPI()

class DocumentationRequest(BaseModel):
    repo_link: str
    sections: List[str]

@app.post("/generate-documentation")
async def generate_documentation(request: DocumentationRequest):
    try:
        # Clone the GitHub repository
        repo_path = "/tmp/repo"
        if os.path.exists(repo_path):
            subprocess.run(["rm", "-rf", repo_path])  # Clean up old clone if exists
        git.Repo.clone_from(request.repo_link, repo_path)

        # Generate documentation based on selected sections
        # Here you could call your existing script and pass the selected sections.
        # Assuming the script is named `generate_docs.py` and accepts args.

        selected_sections = " ".join(request.sections)
        subprocess.run(["python", "generate_docs.py", repo_path, selected_sections])

        return {"message": "Documentation generated successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

