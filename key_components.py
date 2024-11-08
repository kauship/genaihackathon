import os
from langchain.llms import OpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.prompts import PromptTemplate

# Set up project path and OpenAI API key
project_path = "/path/to/spring-petclinic"  # Update with actual project path
openai_api_key = "your_openai_api_key"      # Replace with your OpenAI API key

# Step 1: Collect Java Files for Analysis
java_files = []
for root, dirs, files in os.walk(project_path):
    for file in files:
        if file.endswith(".java"):
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                java_files.append({"filename": file_path, "content": f.read()})

# Step 2: Initialize LLM
llm = OpenAI(model_name="gpt-4-turbo", api_key=openai_api_key)

# Step 3: Define Prompt Templates
class_component_prompt = """
Analyze the following Java class file and generate a detailed summary for each class and its components. 
For each class, include:
- Class Name and its purpose.
- Constructor(s): Description, parameters, and role.
- Methods: For each main method, provide:
    - Method name
    - Parameters (type and description)
    - Return type
    - Functionality and logic
    - Example usage

File Content:
{file_content}
"""

data_structure_prompt = """
Analyze the following Java file for important data structures such as arrays, lists, and maps. 
For each data structure found, provide:
- A description of its purpose
- Any assumptions about the data it contains
- Example usage if available

File Content:
{file_content}
"""

# Step 4: Process Each Java File
key_components_text = "4. Key Code Components\n\n"
for java_file in java_files:
    file_content = java_file['content']
    
    # Generate Class and Method Details
    class_prompt = class_component_prompt.format(file_content=file_content)
    class_details = llm(class_prompt)
    
    # Generate Data Structure Details
    data_structure_prompt_text = data_structure_prompt.format(file_content=file_content)
    data_structure_details = llm(data_structure_prompt_text)
    
    # Combine results for this file
    key_components_text += f"File: {java_file['filename']}\n\n"
    key_components_text += "Classes and Methods:\n" + class_details + "\n"
    key_components_text += "Data Structures:\n" + data_structure_details + "\n\n"

# Step 5: Save Key Code Components to a File
with open("key_code_components.txt", "w") as f:
    f.write(key_components_text)

print("Key Code Components section generated and saved as 'key_code_components.txt'")
