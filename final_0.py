import os
import glob
import concurrent.futures
from typing import List, Dict, Optional
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# Import prompts from prompts.py
from prompts import prompts

def load_and_chunk_file(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 100) -> List[Document]:
    """Loads and chunks a single file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    documents = [Document(page_content=chunk, metadata={"source": file_path}) for chunk in chunks]
    return documents

def load_documents_from_directory(directory_path: str, file_extension: str = "*.java") -> List[Document]:
    """Loads documents from a directory using multithreading and returns a list of Document objects."""
    file_paths = glob.glob(os.path.join(directory_path, '**', file_extension), recursive=True)
    all_documents = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(load_and_chunk_file, file_path) for file_path in file_paths]
        for future in concurrent.futures.as_completed(futures):
            try:
                documents = future.result()
                all_documents.extend(documents)
            except Exception as e:
                print(f"Error loading file: {e}")
    return all_documents

def generate_documentation_section(documents: List[Document], section_name: str, prompt: str, llm: OpenAI) -> str:
    """Generates documentation for a given section using the provided prompt."""
    docs_text = "\n\n".join([doc.page_content for doc in documents])
    response = llm(f"{prompt}\n\n{docs_text}")
    return f"## {section_name}\n\n{response}\n\n"

def generate_and_save_documentation(directory_path: str, output_dir: str, selected_sections: Optional[List[str]] = None) -> Dict[str, str]:
    """Generates a full documentation structure and saves each section as a markdown file."""
    documents = load_documents_from_directory(directory_path)
    
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(documents, embeddings)
    
    llm = OpenAI()

    documentation = {}
    
    os.makedirs(output_dir, exist_ok=True)
    
    for section_name, prompt in prompts.items():
        if selected_sections and section_name not in selected_sections:
            continue
        relevant_docs = vectorstore.similarity_search(prompt, top_k=5)
        section_text = generate_documentation_section(relevant_docs, section_name, prompt, llm)
        documentation[section_name] = section_text
        
        output_file = os.path.join(output_dir, f"{section_name.replace(' ', '_').lower()}.md")
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(section_text)
        print(f"Saved section: {section_name} to {output_file}")
    
    return documentation

project_path = "./path_to_your_codebase"
output_dir = "./docs"
selected_sections = ["Overview", "Getting Started", "Code Structure Overview"]
documentation = generate_and_save_documentation(project_path, output_dir, selected_sections)
