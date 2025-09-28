## what is model context protocol (mcp)
Model Context Protocol (MCP) is a new open standard that defines how applications (like IDEs, chatbots, or other clients) can connect to external tools, data sources, and services in a safe, structured, and interoperable way — so that Large Language Models (LLMs) can use them.
![mcp-simple-diagram](https://github.com/user-attachments/assets/a9c5283d-9e2d-4e15-8248-5b0acb7b4bda)
reference: https://modelcontextprotocol.io/docs/getting-started/intro

## tool integration with LLM (prior mcp)
Before MCP, every LLM app had to invent its own way to connect models to:

Databases

APIs

Developer tools (like running code)

Local files

Cloud services

This caused:

Fragmentation (different systems couldn’t reuse each other’s tools)

Security concerns (random code execution risk)

Lack of portability (a tool written for one app couldn’t be reused elsewhere)

MCP solves this by introducing a shared, standardized protocol.

### code example tool integration without mcp
```
from google import genai
from google.genai import types

from emp_mgmt_operations import add_employee, list_employees

# Define the function declaration for the model
add_employee_function = {
    "name": "add_employee",
    "description": "Adds a new employee to the employee database.",
    "parameters": {
        "type": "object",
        "properties": {
            "emp_name": {
                "type": "string",
                "description": "The name of the employee."
            },
            "emp_role": {
                "type": "string",
                "description": "The role or designation of the employee."
            },
            "emp_city": {
                "type": "string",
                "description": "The city where the employee is located."
            },
            "emp_pincode": {
                "type": "integer",
                "description": "The pincode of the employee's city."
            }
        },
        "required": ["emp_name", "emp_role", "emp_city", "emp_pincode"],
    },
}

list_employee_function = {
    "name": "list_employee",
    "description": "Retrieves a list of all employees from the employee database.",
    }
 

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[add_employee_function, list_employee_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Add a new employee named John Doe, who is a Software Engineer located in New York with pincode 10001.",
    config=config,
)

# Check for a function call
funct_call = response.candidates[0].content.parts[0].function_call
if funct_call:
    print(f"Function to call: {funct_call.name}")
    print(f"Arguments: {funct_call.args}")
    result = add_employee(**funct_call.args)
    print(f"Function result: {result}")
else:
    print("No function call found in the response.")
    print(response.text)

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="list all employees.",
    config=config,
)

# Check for a function call
funct_call = response.candidates[0].content.parts[0].function_call
if funct_call:
    print(f"Function to call: {funct_call.name}")
    print(f"Arguments: {funct_call.args}")
    result = list_employees()
    print(f"employee list: {result}")
else:
    print("No function call found in the response.")
    print(response.text)
```

## tools integration with LLM (with mcp)
Under mcp method we need not to create tools in declarative style (shown in above code) where we need to prove function descriptions , parameters required by functions.
However, over here we need to just annotate / decorate  the function defination like **@mcp.tool("tool_name")** 

### code example tool integration with mcp server
emp_mgmt_operations.py

```
# mcp tool defination
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

```

llm_with_mcp.py
```
from emp_mgmt_operations import mcp

# Start the MCP server to expose the tools
if __name__ == "__main__":
    mcp.run(transport='stdio')
```

### mcp server configuration file
mcp.json
```
{
  "servers": {
    "emp_mgmt": {
      "command": "uv",
       "args": [
        "--directory",
        "F:\\coding_education\\model_context_protocol\\employee_mgmt_with_mcp",
        "run",
        "llm_with_mcp.py"
      ]
    }
  }
}
```
