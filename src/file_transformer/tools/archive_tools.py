import os
import zipfile
import mcp.types as types
from ..security import SecurityManager

def get_archive_tool_defs():
    return [
        types.Tool(
            name="zip_files",
            description="Create a ZIP archive from multiple files.",
            inputSchema={
                "type": "object",
                "properties": {
                    "paths": {"type": "array", "items": {"type": "string"}},
                    "out_zip": {"type": "string"},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["paths", "out_zip"],
            },
        ),
    ]

async def handle_archive_tools(name: str, arguments: dict, security: SecurityManager) -> list[types.TextContent]:
    if name == "zip_files":
        paths = arguments.get("paths", [])
        out_zip = arguments.get("out_zip")
        dry_run = arguments.get("dry_run", False)
        
        if not paths or not out_zip:
            return [types.TextContent(type="text", text="Error: paths and out_zip are required.")]
            
        try:
            safe_paths = []
            for path in paths:
                safe_path = security.validate_path(path)
                security.check_file_size(safe_path)
                safe_paths.append(safe_path)
                
            safe_out_zip = security.validate_path(out_zip)
            security.ensure_directory(safe_out_zip)
            
            if dry_run:
                return [types.TextContent(type="text", text=f"[DRY RUN] Would zip {len(paths)} files into {out_zip}")]
            
            with zipfile.ZipFile(safe_out_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in safe_paths:
                    zipf.write(file, os.path.basename(file))
                    
            return [types.TextContent(type="text", text=f"Zipped {len(paths)} files into {out_zip}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
            
    return []
