import os
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import json

# Set up paths and OpenAI API key
project_path = "/path/to/spring-petclinic"  # Update with actual path to the project
openai_api_key = "your_openai_api_key"      # Replace with your OpenAI API key

# Step 1: Generate File Organization (Directory Structure)

def generate_directory_structure(root_dir, max_depth=3, depth=0):
    if depth > max_depth:
        return None

    dir_structure = {}
    for item in os.listdir(root_dir):
        item_path = os.path.join(root_dir, item)
        if os.path.isdir(item_path):
            dir_structure[item] = generate_directory_structure(item_path, max_depth, depth + 1)
        else:
            dir_structure[item] = None
    return dir_structure

directory_structure = generate_directory_structure(project_path)

# Step 2: Load Project Files and README for Module Descriptions
loader = DirectoryLoader(project_path, glob="README.md")  # Load README if present
readme_document = loader.load()[0] if loader.load() else None  # Assuming README.md exists

documents = []
for root, dirs, files in os.walk(project_path):
    for file in files:
        if file.endswith(".java") or file in ["pom.xml", "build.gradle"]:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            documents.append({"filename": file_path, "content": content})

# Step 3: Initialize LLM and Define Prompt for Module Breakdown
llm = OpenAI(model_name="gpt-4-turbo", api_key=openai_api_key)

module_breakdown_prompt = """
Given the following files and descriptions from a Spring Boot project, provide a description of each main module or component.
For each module, explain its responsibility within the codebase.

Files:
{file_list}

README Content (if available):
{readme_content}
"""

file_list = "\n".join([doc["filename"] for doc in documents])
readme_content = readme_document.page_content if readme_document else "README not available"

module_breakdown_text = module_breakdown_prompt.format(file_list=file_list, readme_content=readme_content)
module_breakdown = llm(module_breakdown_text)

# Step 4: Generate Flow Diagrams
# Prompt to create a Mermaid sequence diagram to represent app flow and module interactions
flow_diagram_prompt = """
Using Mermaid syntax, generate a flowchart or sequence diagram based on the following project structure and module responsibilities.

Directory Structure:
{directory_structure}

Module Breakdown:
{module_breakdown}

Represent the main flow of the application, including how different modules interact in the sequence diagram. Use high-level module names rather than specific functions.
"""

flow_diagram_text = flow_diagram_prompt.format(
    directory_structure=json.dumps(directory_structure, indent=2),
    module_breakdown=module_breakdown
)

flow_diagram = llm(flow_diagram_text)

# Step 5: Combine All Parts into a "Code Structure Overview" Section
code_structure_overview = f"""
3. Code Structure Overview

File Organization:
{json.dumps(directory_structure, indent=2)}

Module Breakdown:
{module_breakdown}

Flow Diagrams:
{flow_diagram}
"""

print("Code Structure Overview:\n", code_structure_overview)

# Optional: Save to a file
with open("code_structure_overview.txt", "w") as f:
    f.write(code_structure_overview)
