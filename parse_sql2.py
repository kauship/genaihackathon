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

# Print the parsed structure
print(parsed_tree.to_tree())
