Weather - Stock MCP server
==========================
Built for demonstrating the working of MCP protocol.

1. Change folder to weather-stock-server

2. Create venv                
uv   venv

3. Source to venv

source .venv/bin/activate

Windows:
. .venv/Scripts/activate

4. Add packages

uv add mcp

uv add mcp[cli]

5. Launch server

Dev mode i.e., with inspector:
uv run mcp dev server.py


SSE Server
==========
1. Change the server code to support the SSE transport
2. Launch the server as an independent process

python ./server.py

3. open inspector in browser

npx @modelcontextprotocol/inspector 

4. Switch the protocol to SSE and connect

5. Try out the tools/resources & prompts
