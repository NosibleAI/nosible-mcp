![Logo](https://github.com/NosibleAI/nosible-py/blob/main/docs/_static/readme.png?raw=true)

# NOSIBLE MPC Server

MCP server for the [NOSIBLE Search API](https://www.nosible.ai/search/v2/docs/#/).
Uses the [NOSIBLE client package](https://nosible-py.readthedocs.io/).

***

### Usage:

- Using with Claude Desktop:
```json
{
  "mcpServers": {
    "nosible-demo": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://nosible-mcp.onrender.com/mcp/",
        "--header",
        "X-Nosible-Api-Key:${NOSIBLE_API_KEY}"
      ],
      "env": {
        "NOSIBLE_API_KEY": "your-real-key"
      }
    }
  }
}
```

- Using with Cursor:
```json
{
  "mcpServers": {
    "nosible-demo": {
      "type": "http",
      "url": "https://nosible-mcp.onrender.com/mcp/",
      "headers": {
        "X-Nosible-Api-Key": "${NOSIBLE_API_KEY}"
      }
    }
  }
}
```

### Developer Usage
Run the server:
```commandline
python src/server.py
```
