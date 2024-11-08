import os
import json
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Set up project path and OpenAI API key
project_path = "/path/to/spring-petclinic"  # Replace with actual path
openai_api_key = "your_openai_api_key"      # Replace with your OpenAI API key
llm = OpenAI(model_name="gpt-4-turbo", api_key=openai_api_key)

# Step 1: Load Code Files
java_files = []
for root, dirs, files in os.walk(project_path):
    for file in files:
        if file.endswith(".java"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                java_files.append({"filename": file_path, "content": f.read()})

# Step 2: Define Prompts for Each Documentation Section

# Prompts for Function and API Documentation
function_prompt = """
For each function in the following Java file, provide:
- Function signature (name, return type, parameters)
- Detailed description, side effects, and dependencies
- Example input and output

File Content:
{file_content}
"""

api_prompt = """
For each API endpoint in the following Java file, provide:
- Endpoint URL and HTTP method (GET, POST, etc.)
- Description of the endpoint
- Parameters (required and optional), types, and formats
- Response format, status codes, and error messages

File Content:
{file_content}
"""

# Prompts for Error Handling and Logging
error_logging_prompt = """
Analyze the following Java file for error handling and logging mechanisms. 
Describe:
- Exception handling (e.g., try/catch blocks, custom error messages)
- Common error codes or exceptions and their meanings
- Logging system: what events or errors are logged, and how to interpret log messages

File Content:
{file_content}
"""

# Prompts for Dependencies, Configuration, and Other Sections
dependency_prompt = "List all external libraries, internal dependencies, and versions used in the code."
config_prompt = "Summarize configuration files, environment variables, and custom settings in the code."
performance_prompt = "Describe performance optimizations, scalability features, and benchmarks in the code."
testing_prompt = "Summarize the testing strategy, test coverage, and key test cases in the code."
security_prompt = "Summarize sensitive data handling, access control, and security vulnerabilities in the code."
version_control_prompt = "Summarize the git history and changelog for the project."
faq_prompt = "List common questions and troubleshooting steps for this codebase."
glossary_prompt = "Create a glossary of key terms used in the code."
conclusion_prompt = "Provide a brief summary of the documentation, including key points and recommendations."

# Step 3: Generate Documentation Content
documentation = ""

for java_file in java_files:
    file_content = java_file["content"]
    
    # Generate Function Documentation
    function_doc = llm(function_prompt.format(file_content=file_content))
    documentation += f"File: {java_file['filename']}\n\nFunctions:\n{function_doc}\n\n"

    # Generate API Documentation (if applicable)
    api_doc = llm(api_prompt.format(file_content=file_content))
    documentation += f"API Endpoints:\n{api_doc}\n\n"

    # Generate Error Handling and Logging Section
    error_logging_doc = llm(error_logging_prompt.format(file_content=file_content))
    documentation += f"Error Handling and Logging:\n{error_logging_doc}\n\n"

# Additional sections
dependency_doc = llm(dependency_prompt)
config_doc = llm(config_prompt)
performance_doc = llm(performance_prompt)
testing_doc = llm(testing_prompt)
security_doc = llm(security_prompt)
version_control_doc = llm(version_control_prompt)
faq_doc = llm(faq_prompt)
glossary_doc = llm(glossary_prompt)
conclusion_doc = llm(conclusion_prompt)

# Combine all sections into final documentation
documentation += f"Dependencies:\n{dependency_doc}\n\n"
documentation += f"Configuration:\n{config_doc}\n\n"
documentation += f"Performance Considerations:\n{performance_doc}\n\n"
documentation += f"Testing and Quality Assurance:\n{testing_doc}\n\n"
documentation += f"Security Considerations:\n{security_doc}\n\n"
documentation += f"Version Control and Changelog:\n{version_control_doc}\n\n"
documentation += f"FAQ:\n{faq_doc}\n\n"
documentation += f"Appendix:\nGlossary:\n{glossary_doc}\n\n"
documentation += f"Conclusion:\n{conclusion_doc}\n\n"

# Save to file
with open("full_documentation.txt", "w") as f:
    f.write(documentation)

print("Documentation generated and saved as 'full_documentation.txt'")
