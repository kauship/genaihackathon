import os
import re
import graphviz

def find_java_files(project_dir):
    """Find all Java files in the project directory."""
    java_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files

def parse_imports(java_file):
    """Parse import statements in a Java file to find dependencies."""
    imports = []
    with open(java_file, 'r') as f:
        for line in f:
            # Match lines that start with 'import ' and capture the class path
            match = re.match(r'import\s+([a-zA-Z0-9_.]+);', line)
            if match:
                imports.append(match.group(1))
    return imports

def get_class_name(java_file):
    """Extract the class name from a Java file path."""
    with open(java_file, 'r') as f:
        for line in f:
            match = re.match(r'(public\s+)?class\s+([A-Za-z0-9_]+)', line)
            if match:
                return match.group(2)
    return None

def build_dependency_graph(project_dir):
    """Build a dependency graph for the Java project."""
    # Initialize a directed graph using Graphviz
    graph = graphviz.Digraph(comment="Project Flow Diagram", format="png")
    
    # Create a mapping from class names to their dependencies
    dependencies = {}
    java_files = find_java_files(project_dir)
    
    for java_file in java_files:
        class_name = get_class_name(java_file)
        if class_name:
            imports = parse_imports(java_file)
            dependencies[class_name] = imports

    # Add nodes and edges to the graph
    for class_name, imports in dependencies.items():
        graph.node(class_name)  # Add the class as a node in the graph
        for imp in imports:
            imported_class = imp.split('.')[-1]  # Only use the class name
            if imported_class in dependencies:
                graph.edge(class_name, imported_class)  # Add a directed edge
    
    return graph

def save_diagram(graph, output_path="project_flow_diagram"):
    """Save the generated graph as an image file."""
    graph.render(filename=output_path, cleanup=True)
    print(f"Flow diagram saved to {output_path}.png")

def main():
    # Set your project directory path here
    project_dir = "/path/to/your/java/project"
    
    # Build the dependency graph
    graph = build_dependency_graph(project_dir)
    
    # Save the flow diagram
    save_diagram(graph)

if __name__ == "__main__":
    main()
