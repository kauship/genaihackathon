# prompts.py

def overview_of_code_prompt():
    """
    Generates a prompt to create an overview of the codebase.
    """
    return (
        "Provide a high-level overview of the codebase, describing its purpose, "
        "main components, and functionality. Highlight key aspects and unique features, "
        "along with the general architecture and design patterns in use."
    )

def getting_started_prompt():
    """
    Generates a prompt for the Getting Started section.
    """
    return (
        "Provide a Getting Started guide for this codebase. Include the following sections:\n"
        "- Prerequisites: List software dependencies, hardware requirements, and network configurations.\n"
        "- Setup Instructions: Step-by-step guide to set up the environment, install dependencies, and configure the system.\n"
        "- Run Instructions: Describe how to run the application or code, such as starting a server or running a command.\n"
        "- Example Usage: Include simple examples showing how to use the code, including any command-line instructions or API calls."
    )

def code_structure_overview_prompt():
    """
    Generates a prompt for the Code Structure Overview section.
    """
    return (
        "Provide a Code Structure Overview for this project:\n"
        "- File Organization: Visual representation or explanation of the file and folder structure.\n"
        "- Module Breakdown: Describe the main modules or components of the codebase and their responsibilities.\n"
        "- Flow Diagrams: Provide flowcharts or sequence diagrams showing the flow of the application and module interactions."
    )

def key_code_components_prompt():
    """
    Generates a prompt for the Key Code Components section.
    """
    return (
        "Generate detailed documentation for Key Code Components:\n"
        "- Classes and Methods:\n"
        "  - List each class and describe its purpose.\n"
        "  - Explain constructors, parameters, and their role.\n"
        "  - Describe main methods, including:\n"
        "      * Method name\n"
        "      * Parameters (type and description)\n"
        "      * Return type\n"
        "      * Functionality and logic\n"
        "      * Example usage\n"
        "- Data Structures:\n"
        "  - Describe important data structures (e.g., arrays, lists, maps), their purpose, and assumptions about the data."
    )

def functions_and_api_documentation_prompt():
    """
    Generates a prompt for the Functions and API Documentation section.
    """
    return (
        "Generate Functions and API Documentation:\n"
        "- For each function or method, include:\n"
        "  * Signature (name, return type, parameters)\n"
        "  * Detailed description, including side effects or dependencies.\n"
        "  * Example input and output.\n"
        "- For each API endpoint:\n"
        "  * Endpoint URL path and HTTP method (GET, POST, etc.).\n"
        "  * Description of the endpoint's purpose.\n"
        "  * Parameters: Required and optional parameters, their types, and formats.\n"
        "  * Response: Details about the API response, including status codes, data format, and error messages."
    )

def error_handling_logging_prompt():
    """
    Generates a prompt for the Error Handling and Logging section.
    """
    return (
        "Document the Error Handling and Logging:\n"
        "- Exception Handling: Describe mechanisms used (e.g., try/catch blocks, custom error messages).\n"
        "- Error Codes: List common error codes or exceptions and their meanings.\n"
        "- Logging: Overview of the logging system, what events or errors are logged, and how to interpret log messages."
    )

def dependencies_prompt():
    """
    Generates a prompt for the Dependencies section.
    """
    return (
        "List Dependencies for this codebase:\n"
        "- External Libraries: List third-party libraries or frameworks, including version numbers.\n"
        "- Internal Dependencies: Describe how internal components or modules depend on each other.\n"
        "- Versioning: Information on versions of external dependencies and any specific version requirements."
    )

def configuration_prompt():
    """
    Generates a prompt for the Configuration section.
    """
    return (
        "Document Configuration Settings:\n"
        "- Configuration Files: Overview of configuration files and their structure (e.g., .properties, .yml, .json).\n"
        "- Environment Variables: List required environment variables and their purpose.\n"
        "- Custom Settings: Describe customizable settings and their impact on code behavior."
    )

def performance_considerations_prompt():
    """
    Generates a prompt for the Performance Considerations section.
    """
    return (
        "Provide documentation for Performance Considerations:\n"
        "- Optimizations: Describe any optimizations in the codebase and their impact.\n"
        "- Scalability: Information on handling scaling, large data sets, concurrency, and multi-threading.\n"
        "- Benchmarks: Relevant performance benchmarks or tests to understand code efficiency."
    )

def testing_quality_assurance_prompt():
    """
    Generates a prompt for the Testing and Quality Assurance section.
    """
    return (
        "Document Testing and Quality Assurance:\n"
        "- Testing Strategy: Describe the testing approach (unit, integration, end-to-end tests).\n"
        "- Test Coverage: Mention which parts of the code are tested, and any areas with low or no coverage.\n"
        "- Test Cases: Provide examples of important test cases or scenarios with expected inputs and outputs.\n"
        "- Tools: List testing tools or frameworks used (e.g., JUnit, Mockito, Selenium)."
    )

def security_considerations_prompt():
    """
    Generates a prompt for the Security Considerations section.
    """
    return (
        "Document Security Considerations:\n"
        "- Sensitive Data Handling: Describe how sensitive data is managed and protected.\n"
        "- Access Control: Document authentication and authorization mechanisms.\n"
        "- Vulnerabilities: Known vulnerabilities, potential attack vectors, and steps taken to mitigate them."
    )

def version_control_changelog_prompt():
    """
    Generates a prompt for the Version Control and Changelog section.
    """
    return (
        "Provide Version Control and Changelog information:\n"
        "- Git History: Summary of significant commits or changes over time.\n"
        "- Changelog: Track all versions and updates, including new features, bug fixes, and breaking changes."
    )

def faq_prompt():
    """
    Generates a prompt for the FAQ section.
    """
    return (
        "Create an FAQ section:\n"
        "- Common Questions: Address common issues or questions about using the codebase.\n"
        "- Troubleshooting: List common problems and their solutions or workarounds."
    )

def appendix_prompt():
    """
    Generates a prompt for the Appendix section.
    """
    return (
        "Provide an Appendix with the following:\n"
        "- Glossary: Define key terms used in the code or documentation.\n"
        "- References: External documentation, libraries, or resources relevant to understanding the code.\n"
        "- Acknowledgments: Credit contributors, open-source libraries, or tools used."
    )

def conclusion_prompt():
    """
    Generates a prompt for the Conclusion section.
    """
    return (
        "Provide a Conclusion:\n"
        "- Summary: Briefly recap the key points covered in the documentation.\n"
        "- Next Steps: Any recommendations for extending or modifying the code or additional resources."
    )
