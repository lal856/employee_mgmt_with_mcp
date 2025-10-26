# Employee Management Operations using SQLite

from typing import Optional, List, Dict, Any
from mcp.server.fastmcp import FastMCP
from employee_db import Database

mcp = FastMCP("employee_mgmt")


@mcp.tool("add_employee")
def add_employee(
    emp_name: str,
    emp_role: str,
    emp_salary: float,
    emp_city: str,
    emp_pincode: str
) -> str:
    """
    Add a new employee and return confirmation with ID.

    Args:
        emp_name (str): Name of the employee.
        emp_role (str): Role of the employee.
        emp_salary (float): Salary of the employee.
        emp_city (str): City of the employee.
        emp_pincode (str): Pincode of the employee.

    Returns:
        str: Confirmation message with the new employee ID.
    """
    db = Database('employees.db')
    emp_id = db.create_employee(emp_name, emp_role, emp_salary, emp_city, emp_pincode)
    return f"Employee added with ID: {emp_id}"


@mcp.tool("update_employee")
def update_employee(
    emp_id: int,
    emp_name: str,
    emp_role: str,
    emp_salary: float,
    emp_city: str,
    emp_pincode: str
) -> str:
    """
    Update employee details by ID. Only provided fields are changed.

    Args:
        emp_id (int): ID of the employee to update.
        emp_name (str): Updated name of the employee.
        emp_role (str): Updated role of the employee.
        emp_salary (float): Updated salary of the employee.
        emp_city (str): Updated city of the employee.
        emp_pincode (str): Updated pincode of the employee.

    Returns:
        str: Confirmation message or not found message.
    """
    db = Database('employees.db')
    success = db.update_employee(emp_id, emp_name, emp_role, emp_salary, emp_city, emp_pincode)
    if success:
        return f"Employee updated with ID: {emp_id}"
    else:
        return f"Employee with ID {emp_id} not found."


@mcp.tool("remove_employee")
def remove_employee(emp_id: int) -> str:
    """
    Remove employee by ID.

    Args:
        emp_id (int): ID of the employee to remove.

    Returns:
        str: Confirmation message or not found message.
    """
    db = Database('employees.db')
    success = db.delete_employee(emp_id)
    if success:
        return f"Employee with ID {emp_id} removed."
    else:
        return f"Employee with ID {emp_id} not found."


@mcp.tool("get_employee")
def get_employee(emp_id: int) -> Optional[Dict[str, Any]]:
    """
    Get employee details by ID.

    Args:
        emp_id (int): ID of the employee to retrieve.

    Returns:
        Optional[Dict[str, Any]]: Employee details as a dictionary, or None if not found.
    """
    db = Database('employees.db')
    employee = db.get_employee(emp_id)
    if employee:
        return employee
    else:
        return None


@mcp.tool("list_employees")
def list_employees() -> List[Dict[str, Any]]:
    """
    Return all employees as a list of dicts.

    Returns:
        List[Dict[str, Any]]: List of all employee records as dictionaries.
    """
    db = Database('employees.db')
    employees = db.list_employees()
    return employees


