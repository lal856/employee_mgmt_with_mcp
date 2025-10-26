# write sqlite database connection code here which supports CRUD operations
import sqlite3
from typing import Any, Optional

class Database:
    def __init__(self, db_file: str):
        """
        Initialize the Database instance.

        Args:
            db_file (str): Path to the SQLite database file.
        """
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        """
        Initialize the database schema by creating the employees table if it does not exist.
        """
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    salary REAL NOT NULL,
                    city TEXT,
                    pincode TEXT
                ) 
                """
            )

    def create_employee(self, name: str, position: str, salary: float, city: str, pincode: str) -> int:
        """
        Insert a new employee record into the database.

        Args:
            name (str): Employee's name.
            position (str): Employee's position.
            salary (float): Employee's salary.
            city (str): Employee's city.
            pincode (str): Employee's pincode.

        Returns:
            int: The ID of the newly created employee.
        """
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO employees (name, position, salary, city, pincode) VALUES (?, ?, ?, ?, ?)",
                (name, position, salary, city, pincode)
            )
            return cursor.lastrowid

    def get_employee(self, employee_id: int) -> Optional[sqlite3.Row]:
        """
        Retrieve an employee record by ID.

        Args:
            employee_id (int): The ID of the employee to retrieve.

        Returns:
            Optional[sqlite3.Row]: The employee record if found, else None.
        """
        cursor = self.conn.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        )
        return cursor.fetchone()

    def update_employee(self, employee_id: int, name: str, position: str, salary: float, city: str, pincode: str) -> bool:
        """
        Update an existing employee's details.

        Args:
            employee_id (int): The ID of the employee to update.
            name (str): New name for the employee.
            position (str): New position for the employee.
            salary (float): New salary for the employee.
            city (str): New city for the employee.
            pincode (str): New pincode for the employee.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        with self.conn:
            cursor = self.conn.execute(
                "UPDATE employees SET name = ?, position = ?, salary = ?, city = ?, pincode = ? WHERE id = ?",
                (name, position, salary, city, pincode, employee_id)
            )
            return cursor.rowcount > 0


    def list_employees(self) -> list[sqlite3.Row]:
        """
        Retrieve all employee records.

        Returns:
            list[sqlite3.Row]: A list of all employee records.
        """
        emp_dict_list = []
        cursor = self.conn.execute("SELECT * FROM employees")
        for emp in cursor.fetchall():
            emp_dict_list.append(dict(emp))
        return emp_dict_list

    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete an employee record by ID.

        Args:
            employee_id (int): The ID of the employee to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        with self.conn:
            cursor = self.conn.execute(
                "DELETE FROM employees WHERE id = ?",
                (employee_id,)
            )
            return cursor.rowcount > 0

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

# Example usage:
# db = Database('employees.db')
# employee_id = db.create_employee("John Doe", "Software Engineer", 75000, "New York", "10001")
# employee = db.get_employee(employee_id)
# print(dict(employee) if employee else "Employee not found.")
# db.update_employee(employee_id, "John Doe", "Senior Software Engineer", 80000, "New York", "10001")
# employee = db.get_employee(employee_id)
# print(dict(employee) if employee else "Employee not found.")
# is_deleted = db.delete_employee(employee_id)
# print("Employee deleted." if is_deleted else "Employee not found.")
# listed_employees = db.list_employees()
# for emp in listed_employees:
#     print(dict(emp))
