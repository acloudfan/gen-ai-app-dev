# create-sqlite-db.py
# This to create a database that will be used for trying out Sqlite MCP server

import sqlite3
import os

# Define the database file name
DB_FILE = "./data/employee_database.db"

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, SQLite version: {sqlite3.sqlite_version}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        print("Table created successfully.")
    except sqlite3.Error as e:
        print(e)

def insert_sample_data(conn):
    """Insert sample data into the employee table."""
    employees = [
        (1, 'John', 'Doe', '1990-05-15', 'Engineering', None, 75000),
        (2, 'Jane', 'Smith', '1988-08-22', 'Marketing', None, 68000),
        (3, 'Peter', 'Jones', '1995-01-30', 'Engineering', 1, 60000),
        (4, 'Alice', 'Williams', '1992-11-11', 'Sales', 2, 72000),
        (5, 'Bob', 'Brown', '1985-03-25', 'Engineering', 1, 90000),
        (6, 'Charlie', 'Davis', '1998-07-07', 'Marketing', 2, 55000)
    ]
    sql = ''' INSERT INTO employee(emp_id, fname, lname, dob, department, manager_emp_id, salary)
              VALUES(?,?,?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.executemany(sql, employees)
        conn.commit()
        print(f"{cur.rowcount} records inserted successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting data: {e}")

def test_employee_select(conn, emp_id):
    """ Test selecting a specific employee by emp_id.
    :param conn: Connection object
    :param emp_id: Employee ID to select
    """
    sql = "SELECT * FROM employee WHERE emp_id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, (emp_id,))
        row = cur.fetchone()
        if row:
            print(f"\nTest Select for emp_id={emp_id}: Found employee - {row}")
        else:
            print(f"\nTest Select for emp_id={emp_id}: No employee found.")
    except sqlite3.Error as e:
        print(f"\nError during test select for emp_id={emp_id}: {e}")


def main():
    # SQL statement to create the employee table
    sql_create_employee_table = """ CREATE TABLE IF NOT EXISTS employee (
                                        emp_id INTEGER PRIMARY KEY,
                                        fname TEXT NOT NULL,
                                        lname TEXT NOT NULL,
                                        dob TEXT,
                                        department TEXT,
                                        manager_emp_id INTEGER,
                                        salary REAL,
                                        FOREIGN KEY (manager_emp_id) REFERENCES employee (emp_id)
                                    ); """

    # Remove the database file if it exists to start fresh
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        print(f"Removed existing database file: {DB_FILE}")

    # create a database connection
    conn = create_connection(DB_FILE)

    # create tables
    if conn is not None:
        # create employee table
        create_table(conn, sql_create_employee_table)
        # insert sample data
        insert_sample_data(conn)
        # Test selecting an employee
        test_employee_select(conn, 3) # Test with emp_id = 3
        # close the connection
        conn.close()
        print(f"\nDatabase {DB_FILE} created, populated, and tested.")
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
