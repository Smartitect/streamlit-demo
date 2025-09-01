# UV Package Manager Setup Guide

## Overview

[UV](https://docs.astral.sh/uv/) is a modern Python package and project manager developed by Astral. It's designed as a drop-in replacement for pip and pip-tools, offering significantly faster package installation and resolution while providing additional project management capabilities.

### Key Advantages of UV

1. **Speed**: UV is written in Rust and is 10-100x faster than pip for package operations
2. **Python Version Management**: UV can install and manage Python versions directly, not just packages
3. **Unified Tool**: Combines package management, virtual environment creation, and dependency resolution
4. **Drop-in Replacement**: Compatible with existing pip workflows and requirements.txt files
5. **Modern Standards**: Built with modern Python packaging standards (PEP 517, PEP 621) in mind

## Project Configuration

This project uses UV for both Python version management and package installation. UV automatically reads the Python version requirement from `pyproject.toml` and installs the appropriate Python version if needed.

### Core Configuration Files

#### 1. `pyproject.toml`
```toml
[project]
name = "streamlit-demo"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "ipykernel>=6.30.1",
    "jupyter>=1.1.1",
    "matplotlib>=3.10.5",
    "nbformat>=5.10.4",
    "numpy>=2.3.2",
    "plotly>=6.3.0",
    "polars>=1.32.3",
    "pytest>=8.4.1",
    "streamlit>=1.48.1",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/streamlit_demo"]
```

**Key Points:**
- `requires-python = ">=3.12"`: UV uses this to install Python 3.12+ automatically
- `name = "streamlit-demo"`: Project name (must match directory structure for local packages)
- `packages = ["src/streamlit_demo"]`: Defines the local package location

#### 2. `.python-version`
```
3.12
```
This file specifies the exact Python version for the project. UV respects this file for version pinning.

#### 3. `.devcontainer/devcontainer.json`
```json
{
    "name": "Ubuntu",
    "image": "mcr.microsoft.com/devcontainers/base:noble",
    "postCreateCommand": "curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc && uv sync",
    "containerEnv": {
        "UV_CACHE_DIR": "/workspaces/streamlit-demo/.uv-cache"
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-toolsai.jupyter",
                "ms-python.python"
            ],
            "settings": {
                "files.exclude": {
                    ".uv-cache": true
                }
            }
        }
    }
}
```

**Key Configuration:**
- `postCreateCommand`: Installs UV and automatically syncs all project dependencies
- `UV_CACHE_DIR`: Sets cache location to resolve filesystem hardlink issues
- `files.exclude`: Hides `.uv-cache` directory from VS Code file explorer

#### 4. `.gitignore`
```gitignore
# UV cache directory
.uv-cache/
```
Prevents committing the local cache directory to version control.

## Local Package Configuration

### Critical Naming Convention

**⚠️ IMPORTANT**: The local package name in `pyproject.toml` must match the source directory structure:

- **Project name**: `streamlit-demo` (in `pyproject.toml`)
- **Source directory**: `src/streamlit_demo/` (underscore, not hyphen)
- **Package specification**: `packages = ["src/streamlit_demo"]`

This naming consistency is crucial for UV to correctly:
1. Build the local package
2. Install it in editable mode
3. Resolve dependencies properly

### Directory Structure
```
streamlit-demo/                 # Project root
├── src/
│   └── streamlit_demo/         # Package name (underscore)
│       ├── __init__.py
│       ├── titanic_wrangler.py
│       └── charting_helper.py
├── pyproject.toml              # Project name with hyphen
└── .uv-cache/                  # Local UV cache
```

**Common Troubleshooting**: If you encounter build errors, verify that:
- The `name` in `pyproject.toml` matches your project
- The `packages` path in `[tool.hatch.build.targets.wheel]` points to the correct source directory
- Directory names use underscores while project names can use hyphens

## Filesystem Hardlink Issue Resolution

### Problem
In WSL Ubuntu devcontainers, UV may display warnings:
```
warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
If the cache and target directories are on different filesystems, hardlinking may not be supported.
```

### Root Cause
- **Project directory**: `/workspaces/streamlit-demo` (ext4 filesystem)
- **Default UV cache**: `/home/vscode/.cache/uv` (overlay filesystem)
- **Issue**: Hardlinks cannot span different filesystems

### Solution
Set `UV_CACHE_DIR` to a location on the same filesystem as the project:

```json
"containerEnv": {
    "UV_CACHE_DIR": "/workspaces/streamlit-demo/.uv-cache"
}
```

This ensures both the project files and UV cache are on the same ext4 filesystem, enabling hardlink operations and maintaining UV's performance benefits.

## Common UV Commands

### Project Setup
```bash
# Install dependencies and create virtual environment
uv sync

# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev pytest

# Remove a dependency
uv remove package-name
```

### Python Version Management
```bash
# Install a specific Python version
uv python install 3.12

# List available Python versions
uv python list

# Pin Python version for project
uv python pin 3.12
```

### Running Commands
```bash
# Run Python with project dependencies
uv run python script.py

# Run tests
uv run pytest

# Start Jupyter notebook
uv run jupyter notebook
```

## Benefits in This Environment

1. **Automatic Setup**: Complete project setup on devcontainer creation - no manual steps required
2. **Automatic Python Management**: UV installs Python 3.12 as specified in `pyproject.toml`
3. **Fast Dependency Resolution**: Significantly faster than pip in devcontainers
4. **Editable Local Package**: Automatically installs `streamlit-demo` in development mode
5. **Cross-Platform Consistency**: Same behavior in devcontainers, local development, and CI
6. **Clean Development Experience**: Cache directory hidden from VS Code file explorer
7. **Modern Project Standards**: Full support for PEP 621 project configuration

## References

- [UV Documentation](https://docs.astral.sh/uv/)
- [UV Project Management](https://docs.astral.sh/uv/concepts/projects/)
- [UV Python Version Management](https://docs.astral.sh/uv/guides/install-python/)
- [PEP 621 - Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
- [UV Cache Configuration](https://docs.astral.sh/uv/configuration/cache/)

## Troubleshooting

### Build Failures
1. Verify project name consistency between `pyproject.toml` and directory structure
2. Check that `packages` specification points to correct source directory
3. Ensure Python version compatibility

### Performance Issues
1. Confirm `UV_CACHE_DIR` is on the same filesystem as the project
2. Check for hardlink warnings and filesystem types with `df -T`

### Dependency Issues
1. Use `uv lock` to regenerate the lock file
2. Clear cache with `uv cache clean` if needed
3. Verify `requires-python` version compatibility