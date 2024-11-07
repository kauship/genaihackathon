import sqlparse
from sqlparse.sql import IdentifierList, Identifier, Parenthesis
from sqlparse.tokens import Keyword, DML, DDL

def extract_identifiers(token_list):
    """Helper to extract table/column identifiers from tokens."""
    identifiers = []
    for token in token_list.tokens:
        if isinstance(token, IdentifierList):
            for identifier in token.get_identifiers():
                identifiers.append(identifier.get_real_name())
        elif isinstance(token, Identifier):
            identifiers.append(token.get_real_name())
        elif isinstance(token, Parenthesis):
            identifiers.extend(extract_identifiers(token))  # Recursive for nested queries
    return identifiers

def parse_stored_procedure(proc_text):
    # Format SQL for better readability
    formatted_proc = sqlparse.format(proc_text, reindent=True, keyword_case='upper')
    
    # Parse the SQL text
    parsed = sqlparse.parse(formatted_proc)
    
    # Initialize the structure to store parsed details
    procedure_summary = {
        'variables': {},
        'statements': [],
        'loops': [],
        'conditions': [],
        'nested_queries': []
    }

    # Track variables declared in the procedure
    current_loop = None
    current_condition = None

    for stmt in parsed:
        stmt_info = {
            'type': None,
            'tables': [],
            'variables_used': [],
            'conditions': [],
            'nested_queries': []
        }

        for token in stmt.tokens:
            # Detect and store declared variables
            if token.ttype is DDL and token.value.upper() == 'DECLARE':
                # Extract declared variables
                var_name = next(token.get_identifiers()).get_real_name()
                procedure_summary['variables'][var_name] = None  # Initialize as None
                
            # Detect and track variable assignments
            elif token.ttype is Keyword and token.value.upper() == 'SET':
                var_name = next(token.get_identifiers()).get_real_name()
                value_token = next(token.get_identifiers())
                procedure_summary['variables'][var_name] = value_token
                
            # Identify and analyze main statement types
            elif token.ttype is DML:
                stmt_info['type'] = token.value.upper()
                stmt_info['tables'] = extract_identifiers(stmt)

            # Detect conditions (IF, CASE, WHERE, etc.)
            if token.ttype is Keyword and token.value.upper() in ['IF', 'WHERE', 'CASE']:
                condition_text = str(token)
                stmt_info['conditions'].append(condition_text)
                procedure_summary['conditions'].append(condition_text)

            # Detect loops (e.g., WHILE loops)
            elif token.ttype is Keyword and token.value.upper() == 'WHILE':
                loop_condition = next(token.get_identifiers())
                procedure_summary['loops'].append({'condition': str(loop_condition), 'body': str(stmt)})
                current_loop = stmt  # Track the loop context

            # Detect nested queries (subqueries)
            if token.is_group and isinstance(token, Parenthesis):
                subquery = str(token).strip('()')
                if 'SELECT' in subquery.upper():
                    stmt_info['nested_queries'].append(subquery)
                    procedure_summary['nested_queries'].append(subquery)

        # Track variables used in each statement
        variables_used = [var for var in procedure_summary['variables'] if var in str(stmt)]
        stmt_info['variables_used'] = variables_used
        procedure_summary['statements'].append(stmt_info)

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
