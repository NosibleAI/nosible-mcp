![Logo](https://github.com/NosibleAI/nosible-py/blob/main/docs/_static/readme.png?raw=true)

# NOSIBLE MPC Server

MCP server for the [NOSIBLE Search API](https://www.nosible.ai/search/v2/docs/#/).
Uses the [NOSIBLE client package](https://nosible-py.readthedocs.io/).

***

### Usage:

- Log on to [NOSIBLE](https://www.nosible.ai/search-api) and retrieve your API key

- Using with VSCode
    - Create a `.vscode/mcp.json` file in your workspace.
    - Select the `Add Server` button to add a template with your own API key for a new server. It should look like this:
```json
{
  "servers": {
    "nosible-demo": {
      "type": "http",
      "url": "https://nosible-mcp.onrender.com/mcp/",
      "headers": {
        "X-Nosible-Api-Key": "YOUR_NOSIBLE_API_KEY_HERE"
      }
    }
  }
}
```

- Using with Claude Desktop:
  - Go to `settings` -> `developer` -> `Edit config`
  - Open `claude_desktop_config.json` and add the following code below, including your API key.
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
        "NOSIBLE_API_KEY": "YOUR_NOSIBLE_API_KEY_HERE"
      }
    }
  }
}
```

- Using with Cursor:
  - Go to `Cursor Settings` -> `MCP & Integrtions` -> `New MCP Server`
  - Add this template below, with your own API key.
```json
{
  "mcpServers": {
    "nosible-demo": {
      "type": "http",
      "url": "https://nosible-mcp.onrender.com/mcp/",
      "headers": {
        "X-Nosible-Api-Key": "YOUR_NOSIBLE_API_KEY_HERE"
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
