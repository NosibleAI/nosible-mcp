# NOSIBLE MPC Server

MCP server for the NOSIBLE Search API

Usage with Claude Desktop:

Example with my dir path, replace with your own: 

```
{
  "mcpServers": {
    "nosible-mcp": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\Users\RichardTaylor\Desktop\MCP\nosible-mcp", 
        "run",
        "main.py"
      ]
    }
  }
}
```

Run with inspector:
```commandline
uv run mcp dev nosible_mcp.py:mcp  
```
