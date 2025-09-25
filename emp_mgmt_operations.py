import random
"""This module contains operations related to employee management."""

employee_database = []

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

def remove_employee(employee_id):
    """
    Removes an employee from the database by their ID.

    Args:
        employee_id (int or str): The unique identifier of the employee to be removed.

    Returns:
        str: A confirmation message indicating the employee has been removed.
    """
   
    employee_database = [emp for emp in employee_database if emp['id'] != employee_id]
    return f"Employee with ID {employee_id} removed."

def get_employee(employee_id):
    """
    Retrieve an employee's information from the employee database by their ID.
    Args:
        employee_id (int or str): The unique identifier of the employee to retrieve.
    Returns:
        dict or None: The employee's information as a dictionary if found, otherwise None.
    """
    
    for emp in employee_database:
        if emp['id'] == employee_id:
            return emp
    return None

def list_employees():
    """
    Retrieve the list of all employees from the employee database.
    Returns:
        list: A list containing all employee records.
    """
    return employee_database


