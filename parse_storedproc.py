import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Parenthesis
from sqlparse.tokens import Keyword, DML, DDL, Name, Whitespace, Comparison, String, Punctuation

def extract_identifiers(token):
    """Helper to extract table/column identifiers from tokens."""
    identifiers = []
    if isinstance(token, IdentifierList):
        for identifier in token.get_identifiers():
            identifiers.append(identifier.get_real_name())
    elif isinstance(token, Identifier):
        identifiers.append(token.get_real_name())
    elif isinstance(token, Parenthesis):
        identifiers.extend(extract_identifiers(token))
    return identifiers

def parse_stored_procedure(proc_text):
    # Format SQL for better readability
    formatted_proc = sqlparse.format(proc_text, reindent=True, keyword_case='upper')
    
    # Parse the SQL text
    parsed = sqlparse.parse(formatted_proc)
    
    # Initialize structure to store parsed details
    procedure_summary = {
        'variables': {},
        'statements': [],
        'loops': [],
        'conditions': [],
        'nested_queries': []
    }

    for stmt in parsed:
        stmt_info = {
            'type': None,
            'tables': [],
            'variables_used': [],
            'conditions': [],
            'nested_queries': []
        }

        # Process tokens within the statement
        token_iterator = iter(stmt.tokens)
        for token in token_iterator:
            print(f"Token: {token}, Type: {token.ttype}")  # Debug: print each token

            # Detect and store declared variables
            if token.ttype is DDL and token.value.upper() == 'DECLARE':
                next_token = next(token_iterator, None)
                if next_token and isinstance(next_token, Identifier):
                    var_name = next_token.get_real_name()
                    procedure_summary['variables'][var_name] = None
                    print(f"Declared Variable: {var_name}")  # Debug: variable declaration

            # Track variable assignments (SET statements)
            elif token.ttype is Keyword and token.value.upper() == 'SET':
                var_name = next(token_iterator, None)
                if var_name and isinstance(var_name, Identifier):
                    var_name = var_name.get_real_name()
                    assignment_value = next(token_iterator, None)
                    if assignment_value:
                        procedure_summary['variables'][var_name] = str(assignment_value)
                        print(f"Assigned Variable: {var_name} = {assignment_value}")  # Debug: variable assignment

            # Identify main statement types (SELECT, INSERT, UPDATE, DELETE)
            elif token.ttype is DML:
                stmt_info['type'] = token.value.upper()
                stmt_info['tables'] = extract_identifiers(stmt)
                print(f"Statement Type: {stmt_info['type']}, Tables: {stmt_info['tables']}")  # Debug: statement type
                
            # Capture conditions (IF, WHERE, CASE)
            elif token.ttype is Keyword and token.value.upper() in ['IF', 'WHERE', 'CASE']:
                condition_text = str(token)
                stmt_info['conditions'].append(condition_text)
                procedure_summary['conditions'].append(condition_text)
                print(f"Condition Detected: {condition_text}")  # Debug: condition

            # Detect and analyze loops (e.g., WHILE)
            elif token.ttype is Keyword and token.value.upper() == 'WHILE':
                loop_condition = next(token_iterator, None)
                if loop_condition:
                    loop_condition_text = str(loop_condition)
                    procedure_summary['loops'].append({
                        'condition': loop_condition_text,
                        'body': str(stmt)
                    })
                    print(f"Loop Detected: {loop_condition_text}")  # Debug: loop condition

            # Capture nested queries within parentheses
            elif token.is_group and isinstance(token, Parenthesis):
                subquery = str(token).strip('()')
                if 'SELECT' in subquery.upper():
                    stmt_info['nested_queries'].append(subquery)
                    procedure_summary['nested_queries'].append(subquery)
                    print(f"Nested Query Detected: {subquery}")  # Debug: nested query

        # Track variables used in each statement
        variables_used = [var for var in procedure_summary['variables'] if var in str(stmt)]
        stmt_info['variables_used'] = variables_used
        procedure_summary['statements'].append(stmt_info)
        print(f"Statement Info: {stmt_info}")  # Debug: statement info

    return formatted_proc, procedure_summary

# Example Usage for Sybase Procedure
sybase_proc_text = """
CREATE PROCEDURE ExampleProcedure
AS
BEGIN
    DECLARE @ExampleVar INT
    SET @ExampleVar = 1
    
    WHILE @ExampleVar < 5
    BEGIN
        IF @ExampleVar = 1
        BEGIN
            SELECT * FROM Table1 WHERE Column1 = @ExampleVar
        END
        ELSE
        BEGIN
            UPDATE Table2 SET Column2 = 'Value' WHERE Column3 = @ExampleVar
        END
        SET @ExampleVar = @ExampleVar + 1
    END
END
"""

formatted_text, summary = parse_stored_procedure(sybase_proc_text)

print("Formatted Procedure:\n", formatted_text)
print("\nProcedure Summary:")
print("\nVariables Declared and Initial Values:")
for var, value in summary['variables'].items():
    print(f"  {var}: {value}")

print("\nStatements Analyzed:")
for i, stmt in enumerate(summary['statements']):
    print(f"Statement {i+1}:")
    print("  Type:", stmt['type'])
    print("  Tables:", stmt['tables'])
    print("  Variables Used:", stmt['variables_used'])
    print("  Conditions:", stmt['conditions'])
    print("  Nested Queries:", stmt['nested_queries'])

print("\nLoops Detected:")
for i, loop in enumerate(summary['loops']):
    print(f"  Loop {i+1} Condition:", loop['condition'])
    print("  Loop Body:", loop['body'])

print("\nConditions Detected in Procedure:")
for i, condition in enumerate(summary['conditions']):
    print(f"  Condition {i+1}: {condition}")

print("\nNested Queries Detected in Procedure:")
for i, query in enumerate(summary['nested_queries']):
    print(f"  Nested Query {i+1}: {query}")
