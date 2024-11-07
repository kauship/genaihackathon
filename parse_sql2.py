import sqlglot

# Sample Sybase SQL code (simplified)
sql_code = """
    CREATE PROCEDURE my_proc AS
    BEGIN
        DECLARE @id INT;
        SET @id = 1;
        IF @id = 1
        BEGIN
            SELECT * FROM my_table WHERE id = @id;
        END
    END;
"""

# Parse SQL code
parsed_tree = sqlglot.parse_one(sql_code)

# Helper function to print the AST recursively
def print_ast(node, level=0):
    indent = "  " * level
    print(f"{indent}{node.__class__.__name__}: {node}")

    # Recursively print child nodes if available
    for arg, value in node.args.items():
        print(f"{indent}  {arg}:")
        if isinstance(value, list):
            for v in value:
                print_ast(v, level + 2)
        elif isinstance(value, sqlglot.expressions.Expression):
            print_ast(value, level + 2)
        else:
            print(f"{indent}    {value}")

# Print the parsed tree structure
print_ast(parsed_tree)
