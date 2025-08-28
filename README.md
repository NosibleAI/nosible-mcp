# NOSIBLE MPC Server

MCP server for the NOSIBLE Search API

Using with Claude Desktop:
```json
{
  "mcpServers": {
    "test-nosible": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote@latest",
        "http://localhost:10000/mcp/",
        "--transport", "http-only",
        "--allow-http",
        "--debug"
      ]
    }
  }
}
```

Using with Cursor:
```json
{
  "mcpServers": {
    "test-nosible": {
      "url": "http://localhost:10000/mcp/",
      "type": "http"
    }
  }
}
```

Usage with Claude Desktop:
```commandline
TODO
```

Shoutout to [Alejandro AO's GitHub project](https://github.com/alejandro-ao) for helping me in developing
this project.


Self-hosting:
```commandline
pip install -e .
```

Create .env file:
```commandline
cp .env.example .env
```

Run the server:
```commandline
python src/server.py
```