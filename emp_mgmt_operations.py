import random
from mcp.server.fastmcp import FastMCP


"""This module contains operations related to employee management."""

employee_database = []
mcp = FastMCP("employee_mgmt")

@mcp.tool("add_employee")
def add_employee(emp_name, emp_role, emp_city, emp_pincode):
    """
    Adds a new employee to the employee database.
    Parameters:
        emp_name (str): The name of the employee.
        emp_role (str): The role or designation of the employee.
        emp_city (str): The city where the employee is located.
        emp_pincode (str or int): The pincode of the employee's city.
    Returns:
        str: A confirmation message indicating the employee has been added.
    """
    emp_id = random.randint(1000, 9999)
    employee = {
        'id': emp_id,
        'name': emp_name,
        'role': emp_role,
        'city': emp_city,
        'pincode': emp_pincode
    }
    employee_database.append(employee)
    return f"Employee added with ID: {emp_id}"

@mcp.tool("update_employee")
def update_employee(emp_id, emp_name=None, emp_role=None, emp_city=None, emp_pincode=None):
    """
    Updates an existing employee's information in the database.
    Parameters:
        emp_id (int or str): The unique identifier of the employee to be updated.
        emp_name (str, optional): The new name of the employee.
        emp_role (str, optional): The new role or designation of the employee.
        emp_city (str, optional): The new city where the employee is located.
        emp_pincode (str or int, optional): The new pincode of the employee's city.
    Returns:
        str: A confirmation message indicating the employee has been updated, or an error message if not found.
    """
    for emp in employee_database:
        if emp['id'] == emp_id:
            if emp_name:
                emp['name'] = emp_name
            if emp_role:
                emp['role'] = emp_role
            if emp_city:
                emp['city'] = emp_city
            if emp_pincode:
                emp['pincode'] = emp_pincode
            return f"Employee with ID {emp_id} updated."
    return f"Employee with ID {emp_id} not found."

@mcp.tool("remove_employee")
def remove_employee(emp_id):
    """
    Removes an employee from the database by their ID.

    Args:
        emp_id (int or str): The unique identifier of the employee to be removed.

    Returns:
        str: A confirmation message indicating the employee has been removed.
    """
    global employee_database
    employee_database = [emp for emp in employee_database if emp['id'] != emp_id]
    return f"Employee with ID {emp_id} removed."

@mcp.tool("get_employee")
def get_employee(emp_id):
    """
    Retrieve an employee's information from the employee database by their ID.
    Args:
        emp_id (int or str): The unique identifier of the employee to retrieve.
    Returns:
        dict or None: The employee's information as a dictionary if found, otherwise None.
    """
    
    for emp in employee_database:
        if emp['id'] == emp_id:
            return emp
    return None

@mcp.tool("list_employees")
def list_employees():
    """
    Retrieve the list of all employees from the employee database.
    Returns:
        list: A list containing all employee records.
    """
    return employee_database


