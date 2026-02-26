# File Transformer MCP Server

A Model Context Protocol (MCP) server that provides tools for transforming and manipulating local files.

## Features

- **PDF Transformation**: Merge, split, and extract text from PDFs.
- **Image Transformation**: Resize, convert formats, and compress images.
- **Archiving**: Create zip archives of files.
- **Security**: Directory allowlisting and file size limits.

## Installation

```bash
uv pip install .
```

## Tools

- `merge_pdfs`: Merge multiple PDFs into one.
- `split_pdf`: Split a PDF into smaller files.
- `extract_text`: Extract text content from a PDF.
- `resize_image`: Change image dimensions.
- `convert_image_format`: Change image file format (e.g., PNG to JPG).
- `compress_image`: Reduce image file size.
- `zip_files`: Compress files into a ZIP archive.
