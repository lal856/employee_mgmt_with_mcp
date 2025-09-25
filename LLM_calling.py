from google import genai
from google.genai import types

from emp_mgmt_operations import add_employee

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
        
        

# Configure the client and tools
client = genai.Client()
tools = types.Tool(function_declarations=[add_employee_function])
config = types.GenerateContentConfig(tools=[tools])

# Send request with function declarations
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Add a new employee named John Doe, who is a Software Engineer located in New York with pincode 10001.",
    config=config,
)

# Check for a function call
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print(f"Function to call: {function_call.name}")
    print(f"Arguments: {function_call.args}")
    #  In a real app, you would call your function here:
    result = add_employee(**function_call.args)
    print(f"Function result: {result}")
else:
    print("No function call found in the response.")
    print(response.text)