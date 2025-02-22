import os
from pathlib import Path
from typing import List, Set

def get_directory_structure(
    start_path: str = ".",
    exclude_patterns: Set[str] = None,
    max_depth: int = None
) -> List[str]:
    """
    Generate a formatted string representing the directory structure.
    
    Args:
        start_path: Starting directory path (default: current directory)
        exclude_patterns: Set of patterns to exclude (files/directories)
        max_depth: Maximum depth to traverse (None for unlimited)
    
    Returns:
        List of strings representing the directory structure
    """
    if exclude_patterns is None:
        exclude_patterns = {
            # Version control
            ".git", ".gitignore", ".svn", ".hg",
            # Virtual environments
            "venv", "env", ".env", ".venv",
            # Python
            "__pycache__", "*.pyc", "*.pyo", "*.pyd",
            # Node.js
            "node_modules", "package-lock.json",
            # IDE files
            ".idea", ".vscode", "*.swp",
            # Build directories
            "build", "dist", "*.egg-info",
            # OS files
            ".DS_Store", "Thumbs.db"
        }

    def should_exclude(path: str) -> bool:
        """Check if path should be excluded based on patterns."""
        name = os.path.basename(path)
        return any(
            pattern in name or 
            (pattern.startswith("*.") and name.endswith(pattern[1:]))
            for pattern in exclude_patterns
        )

    def format_directory(
        path: str,
        prefix: str = "",
        current_depth: int = 0
    ) -> List[str]:
        """Recursively format directory structure."""
        if max_depth is not None and current_depth > max_depth:
            return []

        if should_exclude(path):
            return []

        output = []
        try:
            entries = os.listdir(path)
        except PermissionError:
            return [f"{prefix}[Permission Denied]"]
        except FileNotFoundError:
            return [f"{prefix}[Directory Not Found]"]

        # Sort entries to list directories first, then files
        dirs = []
        files = []
        for entry in entries:
            full_path = os.path.join(path, entry)
            if should_exclude(full_path):
                continue
            if os.path.isdir(full_path):
                dirs.append(entry)
            else:
                files.append(entry)

        # Process directories
        for i, dir_name in enumerate(sorted(dirs)):
            full_path = os.path.join(path, dir_name)
            is_last = (i == len(dirs) - 1) and not files
            
            # Add directory name
            output.append(f"{prefix}{'└──' if is_last else '├──'} {dir_name}/")
            
            # Recursively process subdirectory
            subdir_prefix = prefix + ('    ' if is_last else '│   ')
            output.extend(format_directory(full_path, subdir_prefix, current_depth + 1))

        # Process files
        for i, file_name in enumerate(sorted(files)):
            is_last = i == len(files) - 1
            output.append(f"{prefix}{'└──' if is_last else '├──'} {file_name}")

        return output

    # Start the directory traversal from the root
    return format_directory(start_path)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate a clean directory structure visualization.')
    parser.add_argument('--path', default='.', help='Starting directory path')
    parser.add_argument('--max-depth', type=int, help='Maximum depth to traverse')
    parser.add_argument('--exclude', nargs='+', help='Additional patterns to exclude')
    
    args = parser.parse_args()
    
    # Create exclude patterns set
    exclude_patterns = {
        ".git", ".gitignore", ".svn", ".hg",
        "venv", "env", ".env", ".venv",
        "__pycache__", "*.pyc", "*.pyo", "*.pyd",
        "node_modules", "package-lock.json",
        ".idea", ".vscode", "*.swp",
        "build", "dist", "*.egg-info",
        ".DS_Store", "Thumbs.db"
    }
    
    # Add any additional exclude patterns
    if args.exclude:
        exclude_patterns.update(args.exclude)
    
    # Generate and print directory structure
    structure = get_directory_structure(args.path, exclude_patterns, args.max_depth)
    print(f"\nDirectory structure for: {os.path.abspath(args.path)}\n")
    if structure:  # Check if structure is not empty
        print("\n".join(structure))
    else:
        print("No visible files or directories found.")