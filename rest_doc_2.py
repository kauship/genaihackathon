import os
import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.document_loaders import DirectoryLoader
from tqdm import tqdm  # Progress bar for visibility
from pathlib import Path

# Configuration
project_path = "/path/to/spring-petclinic"  # Replace with actual path
output_path = "documentation.json"          # Save as JSON for structured data
openai_api_key = "your_openai_api_key"      # Replace with OpenAI API key
llm_model = OpenAI(model_name="gpt-4-turbo", api_key=openai_api_key)

# Helper function to load Java files from the project directory
def load_java_files(directory):
    java_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    java_files.append({"filename": file_path, "content": f.read()})
    return java_files

# Prompt template functions
def generate_prompt(template_text, file_content):
    return template_text.format(file_content=file_content)

# Define modular prompt templates for each section
prompts = {
    "functions": """
        For each function in the following Java file, provide:
        - Function signature (name, return type, parameters)
        - Detailed description, side effects, and dependencies
        - Example input and output
        File Content:
        {file_content}
    """,
    "api": """
        For each API endpoint in the following Java file, provide:
        - Endpoint URL and HTTP method (GET, POST, etc.)
        - Description of the endpoint
        - Parameters (required and optional), types, and formats
        - Response format, status codes, and error messages
        File Content:
        {file_content}
    """,
    "error_logging": """
        Analyze the following Java file for error handling and logging mechanisms. 
        Describe:
        - Exception handling (e.g., try/catch blocks, custom error messages)
        - Common error codes or exceptions and their meanings
        - Logging system: what events or errors are logged, and how to interpret log messages
        File Content:
        {file_content}
    """,
    # Other prompts (dependencies, configuration, etc.) follow a similar structure...
}

# Function to process each section
def process_section(java_files, section_name):
    section_data = {}
    for java_file in tqdm(java_files, desc=f"Processing {section_name}"):
        prompt = generate_prompt(prompts[section_name], java_file['content'])
        try:
            response = llm_model(prompt)
            section_data[java_file['filename']] = response.strip()
        except Exception as e:
            print(f"Error processing file {java_file['filename']} for {section_name}: {e}")
            section_data[java_file['filename']] = "Error generating content"
    return section_data

# Main function to orchestrate documentation generation
def generate_documentation():
    java_files = load_java_files(project_path)
    documentation = {}
    
    # Process each documentation section
    documentation['functions'] = process_section(java_files, "functions")
    documentation['api'] = process_section(java_files, "api")
    documentation['error_handling'] = process_section(java_files, "error_logging")
    
    # Add other sections in a similar manner, e.g., dependencies, configuration, etc.
    # These can be done by expanding the prompts dictionary and adding them here
    
    return documentation

# Save documentation to JSON file for easier structuring and future formatting
def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"Documentation saved to {filename}")

# Generate documentation and save it
documentation = generate_documentation()
save_to_json(documentation, output_path)
