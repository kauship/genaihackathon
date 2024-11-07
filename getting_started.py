import os
from langchain.document_loaders import DirectoryLoader
from langchain.llms import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Set up paths and OpenAI API key
project_path = "/path/to/spring-petclinic"  # Update with actual path to the project
openai_api_key = "your_openai_api_key"      # Replace with your OpenAI API key

# Step 1: Load README and Config Files
loader = DirectoryLoader(project_path, glob="README.md")  # Load README first
readme_document = loader.load()[0] if loader.load() else None  # Assuming README.md exists

# Load common configuration files (for prerequisites and setup details)
config_files = []
for config_file in ["pom.xml", "build.gradle", "Dockerfile"]:
    config_path = os.path.join(project_path, config_file)
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config_files.append({"filename": config_file, "content": f.read()})

# Step 2: Define LLM and Prompts for Each Section

# Initialize LLM
llm = OpenAI(model_name="gpt-4-turbo", api_key=openai_api_key)

# Prompts
getting_started_template = """
Based on the provided project files and configuration, create a comprehensive "Getting Started" section. This should include:
1. Prerequisites: Any required software, dependencies, or configurations.
2. Setup Instructions: Step-by-step instructions for setting up the environment.
3. Run Instructions: How to run the project.
4. Example Usage: Show a few examples for how to use the application.

Files:
{files_content}

If any sections don't apply, indicate so.
"""

# Use README and configuration files as input
files_content = ""
if readme_document:
    files_content += f"\nREADME.md:\n{readme_document.page_content}\n"
for config in config_files:
    files_content += f"\n{config['filename']}:\n{config['content']}\n"

# Create the final prompt
final_prompt = getting_started_template.format(files_content=files_content)

# Step 3: Generate "Getting Started" Section
getting_started_section = llm(final_prompt)
print("Getting Started Section:\n", getting_started_section)

# Optional: Save to a file
with open("getting_started_section.txt", "w") as f:
    f.write("2. Getting Started\n")
    f.write(getting_started_section)
