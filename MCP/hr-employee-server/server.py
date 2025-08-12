# Test SQL :  INSERT INTO employee (emp_id, fname, lname, dob, department, manager_emp_id, salary) VALUES (7, 'Chuck', 'Nathan', '2009-02-28', 'Intern', 1, 15000);
# Test SQL :  SELECT count(*) FROM employee;
# Test SQL :  SELECT * FROM employee WHERE salary < 70000;

import sqlite3

from mcp.server.fastmcp import FastMCP


DB_FILE = "./data/employee_database.db"

mcp = FastMCP("SQLite Explorer")


@mcp.resource("schema://main")
def get_schema() -> str:
    """Provide the database schema as a resource"""
    conn = sqlite3.connect(DB_FILE)
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(sql[0] for sql in schema if sql[0])


@mcp.tool()
def query_data(sql: str) -> str:
    """Execute SQL SELECT queries safely. Raises error for non-SELECT statements."""

    # Check if the SQL statement is a SELECT query (case-insensitive)
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: Only SQL Select Statements are allowed"

    # Create connection
    conn = sqlite3.connect(DB_FILE)
    try:
        result = conn.execute(sql).fetchall()
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def add_employee(emp_id: int, fname: str, lname: str, dob: str, department: str, manager_emp_id: int, salary: float) -> bool:
    """Adds a new employee record to the database."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        sql = ''' INSERT INTO employee(emp_id, fname, lname, dob, department, manager_emp_id, salary)
                  VALUES(?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, (emp_id, fname, lname, dob, department, manager_emp_id, salary))
        conn.commit()
        print(f"Employee {fname} {lname} (ID: {emp_id}) added successfully.")
        return True
    except sqlite3.Error as e:
        print(f"Error adding employee (ID: {emp_id}): {e}")
        if conn:
            conn.rollback() # Rollback changes on error
        return False
    finally:
        if conn:
            conn.close()


@mcp.tool()
def delete_employee(emp_id: int) -> bool:
    """Deletes an employee record from the database by emp_id."""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        sql = 'DELETE FROM employee WHERE emp_id = ?'
        cur = conn.cursor()
        cur.execute(sql, (emp_id,))
        conn.commit()
        if cur.rowcount > 0:
            print(f"Employee with ID {emp_id} deleted successfully.")
            return True
        else:
            print(f"No employee found with ID {emp_id}.")
            return False
    except sqlite3.Error as e:
        print(f"Error deleting employee (ID: {emp_id}): {e}")
        if conn:
            conn.rollback() # Rollback changes on error
        return False
    finally:
        if conn:
            conn.close()


### Uncomment the following to launch the server with SSE endpoint ##
if __name__ == "__main__":
    mcp.run(transport='sse')