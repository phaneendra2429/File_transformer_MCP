import os
from typing import List
from PyPDF2 import PdfReader, PdfWriter
import mcp.types as types
from ..security import SecurityManager

def get_pdf_tool_defs():
    return [
        types.Tool(
            name="merge_pdfs",
            description="Merge multiple PDF files into a single PDF.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_paths": {"type": "array", "items": {"type": "string"}},
                    "out_path": {"type": "string"},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["pdf_paths", "out_path"],
            },
        ),
        types.Tool(
            name="split_pdf",
            description="Split a PDF file into multiple files every N pages.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_path": {"type": "string"},
                    "every_n_pages": {"type": "integer", "default": 1},
                    "dry_run": {"type": "boolean", "default": False},
                },
                "required": ["pdf_path"],
            },
        ),
        types.Tool(
            name="extract_text",
            description="Extract text from a PDF file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "pdf_path": {"type": "string"},
                },
                "required": ["pdf_path"],
            },
        ),
    ]

async def handle_pdf_tools(name: str, arguments: dict, security: SecurityManager) -> list[types.TextContent]:
    if name == "merge_pdfs":
        pdf_paths = arguments.get("pdf_paths", [])
        out_path = arguments.get("out_path")
        dry_run = arguments.get("dry_run", False)
        
        if not pdf_paths or not out_path:
            return [types.TextContent(type="text", text="Error: pdf_paths and out_path are required.")]
        
        try:
            # Validate and check sizes
            safe_pdf_paths = []
            for path in pdf_paths:
                safe_path = security.validate_path(path)
                security.check_file_size(safe_path)
                safe_pdf_paths.append(safe_path)
            
            safe_out_path = security.validate_path(out_path)
            if os.path.isdir(safe_out_path):
                return [types.TextContent(type="text", text=f"Error: out_path must be a file path, not a directory: {out_path}. Please include a filename (e.g., {os.path.join(out_path, 'merged.pdf')})")]
                
            security.ensure_directory(safe_out_path)
            
            if dry_run:
                return [types.TextContent(type="text", text=f"[DRY RUN] Would merge {len(pdf_paths)} PDFs into {out_path}")]
            
            writer = PdfWriter()
            for path in safe_pdf_paths:
                reader = PdfReader(path)
                for page in reader.pages:
                    writer.add_page(page)
            
            with open(safe_out_path, "wb") as f:
                writer.write(f)
                
            return [types.TextContent(type="text", text=f"Merged {len(pdf_paths)} PDFs into {out_path}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "split_pdf":
        pdf_path = arguments.get("pdf_path")
        every_n_pages = arguments.get("every_n_pages", 1)
        dry_run = arguments.get("dry_run", False)
        
        if not pdf_path:
            return [types.TextContent(type="text", text="Error: pdf_path is required.")]
            
        try:
            safe_path = security.validate_path(pdf_path)
            security.check_file_size(safe_path)
            
            reader = PdfReader(safe_path)
            total_pages = len(reader.pages)
            
            if dry_run:
                num_files = (total_pages + every_n_pages - 1) // every_n_pages
                return [types.TextContent(type="text", text=f"[DRY RUN] Would split {pdf_path} ({total_pages} pages) into {num_files} files.")]
            
            base_name = os.path.splitext(safe_path)[0]
            created_files = []
            
            for i in range(0, total_pages, every_n_pages):
                writer = PdfWriter()
                for j in range(i, min(i + every_n_pages, total_pages)):
                    writer.add_page(reader.pages[j])
                
                out_name = f"{base_name}_part_{i // every_n_pages + 1}.pdf"
                with open(out_name, "wb") as f:
                    writer.write(f)
                created_files.append(out_name)
                
            return [types.TextContent(type="text", text=f"Split PDF into {len(created_files)} files: {', '.join(created_files)}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    elif name == "extract_text":
        pdf_path = arguments.get("pdf_path")
        
        if not pdf_path:
            return [types.TextContent(type="text", text="Error: pdf_path is required.")]
            
        try:
            safe_path = security.validate_path(pdf_path)
            security.check_file_size(safe_path)
            
            reader = PdfReader(safe_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
            return [types.TextContent(type="text", text=text)]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
    
    return []
