# This is the driver file for the employee management operations using LLM and MCP.

from emp_mgmt_operations import mcp

# Start the MCP server to expose the tools
if __name__ == "__main__":
    mcp.run(transport='stdio')