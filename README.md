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

