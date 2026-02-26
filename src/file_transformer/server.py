import asyncio
import os
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
import mcp.types as types
from .security import SecurityManager
from .tools.pdf_tools import get_pdf_tool_defs, handle_pdf_tools
from .tools.image_tools import get_image_tool_defs, handle_image_tools
from .tools.archive_tools import get_archive_tool_defs, handle_archive_tools

# Initialize security manager
security = SecurityManager()

server = Server("file-transformer")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return get_pdf_tool_defs() + get_image_tool_defs() + get_archive_tool_defs()

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict | None) -> list[types.TextContent]:
    """Handle tool calls by dispatching to the appropriate module."""
    if not arguments:
        arguments = {}
        
    # PDF Tools
    pdf_result = await handle_pdf_tools(name, arguments, security)
    if pdf_result:
        return pdf_result
        
    # Image Tools
    image_result = await handle_image_tools(name, arguments, security)
    if image_result:
        return image_result
        
    # Archive Tools
    archive_result = await handle_archive_tools(name, arguments, security)
    if archive_result:
        return archive_result
        
    return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def arun():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="file-transformer",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

def main():
    asyncio.run(arun())

if __name__ == "__main__":
    asyncio.run(main())
