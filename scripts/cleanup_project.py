#!/usr/bin/env python3
"""
Project Cleanup Script for Memory Context Manager v2
This script helps organize and clean up the project directory.
"""

import os
import shutil
import glob
from pathlib import Path

def cleanup_python_cache():
    """Remove Python cache files and directories."""
    print("🧹 Cleaning up Python cache files...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                cache_path = os.path.join(root, dir_name)
                print(f"  Removing: {cache_path}")
                shutil.rmtree(cache_path, ignore_errors=True)
    
    # Remove .pyc and .pyo files
    for pattern in ['*.pyc', '*.pyo']:
        for file_path in glob.glob(pattern, recursive=True):
            print(f"  Removing: {file_path}")
            os.remove(file_path)
    
    print("✅ Python cache cleanup complete!")

def cleanup_docker_files():
    """Consolidate Docker configurations."""
    print("🐳 Consolidating Docker configurations...")
    
    # Keep the main docker-compose.yml and remove duplicates
    docker_files = [
        'docker-compose-shareable.yml',
        'docker-compose-minimal.yml',
        'Dockerfile.shareable'
    ]
    
    for file_path in docker_files:
        if os.path.exists(file_path):
            print(f"  Removing duplicate: {file_path}")
            os.remove(file_path)
    
    print("✅ Docker file consolidation complete!")

def cleanup_documentation():
    """Organize documentation files."""
    print("📚 Organizing documentation...")
    
    # Create docs directory if it doesn't exist
    docs_dir = Path('docs')
    docs_dir.mkdir(exist_ok=True)
    
    # Move documentation files to docs directory
    doc_files = [
        'BRAIN_INTERFACE_GUIDE.md',
        'BRAIN_PLUGIN_STRUCTURE.md',
        'CURSOR_SETUP_COMPLETE.md',
        'DATABASE_INTEGRATION_COMPLETE.md',
        'DOCKER_SETUP.md',
        'SHARING_README.md',
        'TESTING_SUMMARY.md',
        'TOOL_EXECUTION_FLOWS.md'
    ]
    
    for file_path in doc_files:
        if os.path.exists(file_path):
            dest_path = docs_dir / file_path
            print(f"  Moving: {file_path} -> docs/{file_path}")
            shutil.move(file_path, dest_path)
    
    print("✅ Documentation organization complete!")

def cleanup_logs():
    """Clean up logs directory."""
    print("📝 Cleaning up logs directory...")
    
    logs_dir = Path('logs')
    if logs_dir.exists():
        # Remove empty logs directory
        if not any(logs_dir.iterdir()):
            print("  Removing empty logs directory")
            logs_dir.rmdir()
        else:
            print("  Logs directory contains files, keeping it")
    
    print("✅ Logs cleanup complete!")

def create_project_structure():
    """Create a clean project structure."""
    print("🏗️  Creating clean project structure...")
    
    # Create necessary directories
    directories = [
        'docs',
        'scripts',
        'tests',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  Created: {directory}/")
    
    print("✅ Project structure created!")

def create_cleanup_readme():
    """Create a README explaining the cleanup."""
    print("📝 Creating cleanup documentation...")
    
    cleanup_readme = """# Project Cleanup Summary

This project has been cleaned up and organized for better maintainability.

## What Was Cleaned Up

### ✅ Removed
- Python cache files (`__pycache__/`, `*.pyc`, `*.pyo`)
- Duplicate Docker configurations
- Temporary development files

### 📁 Reorganized
- Documentation moved to `docs/` directory
- Docker files consolidated
- Project structure standardized

### 🏗️  New Structure
```
memory-context-manager_v2/
├── docs/           # All documentation files
├── scripts/        # Utility scripts
├── tests/          # Test files
├── config/         # Configuration files
├── plugins/        # Plugin system
├── database/       # Database components
├── src/           # Source code
├── docker-compose.yml  # Main Docker configuration
├── Dockerfile     # Main Dockerfile
├── README.md      # Main project README
└── pyproject.toml # Project configuration
```

## Docker Configuration

The project now uses a single, optimized Docker configuration:
- `docker-compose.yml` - Main development setup
- `Dockerfile` - Production-ready container

## Getting Started

1. **Install dependencies**: `uv sync`
2. **Run with Docker**: `docker-compose up`
3. **Run locally**: `uv run python main.py`

## Cleanup Script

To re-run this cleanup: `python cleanup_project.py`
"""
    
    with open('CLEANUP_SUMMARY.md', 'w') as f:
        f.write(cleanup_readme)
    
    print("✅ Cleanup documentation created!")

def main():
    """Main cleanup function."""
    print("🚀 Starting Memory Context Manager v2 Project Cleanup...")
    print("=" * 60)
    
    try:
        cleanup_python_cache()
        cleanup_docker_files()
        cleanup_documentation()
        cleanup_logs()
        create_project_structure()
        create_cleanup_readme()
        
        print("\n" + "=" * 60)
        print("🎉 Project cleanup completed successfully!")
        print("📁 Check CLEANUP_SUMMARY.md for details")
        print("🔧 Your project is now organized and ready for development!")
        
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
