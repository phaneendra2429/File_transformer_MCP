import os
import pathlib
from typing import List, Optional

# Default sandbox directory in Downloads/mcp_sandbox
DEFAULT_SANDBOX = os.path.join(os.path.expanduser("~"), "Downloads", "mcp_sandbox")
MAX_FILE_SIZE_MB = 50  # 50MB limit

class SecurityManager:
    def __init__(self, allowed_directories: Optional[List[str]] = None):
        if allowed_directories is None:
            # Create default sandbox if it doesn't exist
            os.makedirs(DEFAULT_SANDBOX, exist_ok=True)
            self.allowed_directories = [os.path.abspath(DEFAULT_SANDBOX)]
        else:
            self.allowed_directories = [os.path.abspath(d) for d in allowed_directories]

    def is_path_safe(self, path: str) -> bool:
        """Check if a path is within the allowed directories."""
        abs_path = os.path.abspath(path)
        for allowed_dir in self.allowed_directories:
            if abs_path.startswith(allowed_dir):
                return True
        return False

    def validate_path(self, path: str) -> str:
        """Validate path and return absolute path if safe, else raise ValueError."""
        # Sanitize input: strip quotes and whitespace
        clean_path = path.strip().strip('"').strip("'")
        if not self.is_path_safe(clean_path):
            raise ValueError(f"Access denied: Path '{clean_path}' is outside of allowed directories: {self.allowed_directories}")
        return os.path.abspath(clean_path)

    def check_file_size(self, path: str):
        """Check if file size is within limits."""
        if os.path.exists(path):
            size_mb = os.path.getsize(path) / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                raise ValueError(f"File size exceeds limit: {size_mb:.2f}MB > {MAX_FILE_SIZE_MB}MB")

    def ensure_directory(self, path: str):
        """Ensure the directory for a file exists and is safe."""
        dir_path = os.path.dirname(os.path.abspath(path))
        if not self.is_path_safe(dir_path):
            raise ValueError(f"Access denied: Directory '{dir_path}' is outside of allowed directories")
        os.makedirs(dir_path, exist_ok=True)
