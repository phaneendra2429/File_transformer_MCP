# 🛠️ File Transformer MCP Server

A powerful Model Context Protocol (MCP) server that provides a secure suite of tools for transforming and manipulating local files (PDFs, Images, and Archives).

## 🚀 Quick Start

### 1. Installation
This project uses `uv` for lightning-fast dependency management.
```bash
# Clone the repository and install dependencies
uv pip install -e .
```

### 2. Running the Server
To use this with the **MCP Inspector** or **Claude Desktop**, you must run it through `uv` to ensure the virtual environment is correctly loaded.

**Terminal / Inspector:**
```bash
npx @modelcontextprotocol/inspector uv run file-transformer
```

---

## 🛡️ Security & Sandbox Rules

To protect your system, this server operates under a strict **Sandbox Policy**:

1.  **Default Sandbox**: By default, the server only has access to:
    - `%USERPROFILE%\Downloads\mcp_sandbox`
2.  **Directory Allowlisting**:
    - The server will **refuse** to read or write any file outside of its allowed directories.
    - If a path is provided that is not within the sandbox, the tool will return an "Access Denied" error.
3.  **File Size Limits**:
    - Maximum file size allowed for processing is **50MB**.
    - This prevents memory exhaustion and unintended large-scale operations.
4.  **Automatic Provisioning**:
    - The server will automatically create the `mcp_sandbox` folder in your Downloads if it doesn't already exist.

---

## 🧰 Available Tools

### 📄 PDF Tools
- `merge_pdfs`: Merge multiple PDF files into a single document.
- `split_pdf`: Split a PDF into individual pages or specific ranges.
- `extract_text`: Get clean text content from any PDF.

### 🖼️ Image Tools
- `resize_image`: Scale images to specific dimensions.
- `convert_image_format`: Change formats (e.g., JPEG ↔ PNG ↔ WebP).
- `compress_image`: Optimize file size while maintaining quality.

### 📦 Archive Tools
- `zip_files`: Bundle multiple files or directories into a ZIP archive.

---

## ⚙️ Configuration for Claude Desktop
Add this to your `claude_desktop_config.json`:

```json
"mcpServers": {
  "file-transformer": {
    "command": "uv",
    "args": [
      "--directory",
      "<path_to_project>/File_transfer_MCP",
      "run",
      "file-transformer"
    ]
  }
}
```
