import os
import json
import socket
from mcp.server.fastmcp import FastMCP

# Tell MCP it's behind a trusted proxy
os.environ["MCP_TRUST_PROXY"] = "true"

BLENDER_HOST = os.getenv("BLENDER_HOST", "127.0.0.1")
BLENDER_PORT = int(os.getenv("BLENDER_PORT", "65432"))

mcp = FastMCP("Blender MCP Server")


def send_to_blender(code: str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((BLENDER_HOST, BLENDER_PORT))

    payload = {"code": code}
    client.sendall(json.dumps(payload).encode())

    response = client.recv(65536)
    client.close()

    return json.loads(response.decode())


@mcp.tool()
def execute_blender_code(code: str) -> dict:
    return send_to_blender(code)


# IMPORTANT: trust proxy headers
app = mcp.sse_app(trust_proxy=True)