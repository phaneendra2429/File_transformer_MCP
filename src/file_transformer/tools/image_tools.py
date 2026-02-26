import os
from PIL import Image
import mcp.types as types
from ..security import SecurityManager

def get_image_tool_defs():
    return [
        types.Tool(
            name="resize_image",
            description="Resize an image to specific width and height.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string"},
                    "width": {"type": "integer"},
                    "height": {"type": "integer"},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["image_path", "width", "height"],
            },
        ),
        types.Tool(
            name="convert_image_format",
            description="Convert an image from one format to another (e.g., png to jpg).",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string"},
                    "format": {"type": "string", "enum": ["png", "jpg", "jpeg", "webp"]},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["image_path", "format"],
            },
        ),
        types.Tool(
            name="compress_image",
            description="Compress an image to reduce file size.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {"type": "string"},
                    "quality": {"type": "integer", "minimum": 1, "maximum": 100, "default": 80},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["image_path"],
            },
        ),
    ]

async def handle_image_tools(name: str, arguments: dict, security: SecurityManager) -> list[types.TextContent]:
    if name == "resize_image":
        image_path = arguments.get("image_path")
        width = arguments.get("width")
        height = arguments.get("height")
        dry_run = arguments.get("dry_run", False)
        
        if not image_path or not width or not height:
            return [types.TextContent(type="text", text="Error: image_path, width, and height are required.")]
            
        try:
            safe_path = security.validate_path(image_path)
            security.check_file_size(safe_path)
            
            if dry_run:
                return [types.TextContent(type="text", text=f"[DRY RUN] Would resize {image_path} to {width}x{height}")]
            
            with Image.open(safe_path) as img:
                img_resized = img.resize((width, height))
                base, ext = os.path.splitext(safe_path)
                out_path = f"{base}_{width}x{height}{ext}"
                img_resized.save(out_path)
                
            return [types.TextContent(type="text", text=f"Resized image saved to {out_path}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "convert_image_format":
        image_path = arguments.get("image_path")
        fmt = arguments.get("format")
        dry_run = arguments.get("dry_run", False)
        
        if not image_path or not fmt:
            return [types.TextContent(type="text", text="Error: image_path and format are required.")]
            
        try:
            safe_path = security.validate_path(image_path)
            security.check_file_size(safe_path)
            
            if dry_run:
                return [types.TextContent(type="text", text=f"[DRY RUN] Would convert {image_path} to {fmt}")]
            
            with Image.open(safe_path) as img:
                base, _ = os.path.splitext(safe_path)
                out_path = f"{base}.{fmt.lower()}"
                
                # Handle RGBA to RGB for JPEG
                if fmt.lower() in ["jpg", "jpeg"] and img.mode == "RGBA":
                    img = img.convert("RGB")
                    
                img.save(out_path)
                
            return [types.TextContent(type="text", text=f"Converted image saved to {out_path}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "compress_image":
        image_path = arguments.get("image_path")
        quality = arguments.get("quality", 80)
        dry_run = arguments.get("dry_run", False)
        
        if not image_path:
            return [types.TextContent(type="text", text="Error: image_path is required.")]
            
        try:
            safe_path = security.validate_path(image_path)
            security.check_file_size(safe_path)
            
            if dry_run:
                return [types.TextContent(type="text", text=f"[DRY RUN] Would compress {image_path} with quality={quality}")]
            
            with Image.open(safe_path) as img:
                base, ext = os.path.splitext(safe_path)
                out_path = f"{base}_compressed{ext}"
                
                # Check if it's a format that supports quality
                if ext.lower() in [".jpg", ".jpeg", ".webp"]:
                    img.save(out_path, quality=quality)
                else:
                    # For PNG etc, we can use optimize=True
                    img.save(out_path, optimize=True)
                    
            return [types.TextContent(type="text", text=f"Compressed image saved to {out_path}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
            
    return []
