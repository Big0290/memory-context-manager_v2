# Project Organization Guide

## 🏗️ Current Project Structure

```
memory-context-manager_v2/
├── 📁 docs/                    # All documentation and guides
│   ├── BRAIN_INTERFACE_GUIDE.md
│   ├── BRAIN_PLUGIN_STRUCTURE.md
│   ├── CURSOR_SETUP_COMPLETE.md
│   ├── DATABASE_INTEGRATION_COMPLETE.md
│   ├── DOCKER_SETUP.md
│   ├── SHARING_README.md
│   ├── TESTING_SUMMARY.md
│   └── TOOL_EXECUTION_FLOWS.md
├── 📁 scripts/                 # Utility and maintenance scripts
│   └── cleanup_project.py      # Project cleanup and organization
├── 📁 tests/                   # Test files and test suites
├── 📁 config/                  # Configuration files
├── 📁 plugins/                 # Plugin system and extensions
├── 📁 database/                # Database components and adapters
├── 📁 src/                     # Core source code
├── 📁 brain_memory_store/      # Brain memory storage
├── 🐳 docker-compose.yml       # Main Docker configuration
├── 🐳 Dockerfile               # Production Dockerfile
├── 📖 README.md                # Main project documentation
├── 📦 pyproject.toml           # Project configuration
└── 🔧 .cursorrules             # Cursor IDE configuration
```

## 🧹 Maintenance Guidelines

### Regular Cleanup

Run the cleanup script periodically to maintain organization:

```bash
python3 scripts/cleanup_project.py
```

### What Gets Cleaned Up

- **Python cache files** (`__pycache__/`, `*.pyc`, `*.pyo`)
- **Temporary files** and development artifacts
- **Duplicate configurations** and redundant files

### Adding New Files

- **Documentation**: Place in `docs/` directory
- **Scripts**: Place in `scripts/` directory
- **Tests**: Place in `tests/` directory
- **Configs**: Place in `config/` directory

## 🚀 Development Workflow

### 1. Project Setup

```bash
# Install dependencies
uv sync

# Run with Docker
docker-compose up

# Run locally
uv run python main.py
```

### 2. Adding Features

- Create plugins in `plugins/` directory
- Update documentation in `docs/` directory
- Add tests in `tests/` directory

### 3. Maintenance

- Run cleanup script regularly
- Keep documentation updated
- Maintain consistent file organization

## 📋 File Categories

### Core Application

- `main.py` - Main application entry point
- `brain_interface.py` - Brain interface implementation
- `llm_client.py` - LLM client for AI models

### Configuration

- `pyproject.toml` - Python project configuration
- `docker-compose.yml` - Docker services configuration
- `.cursorrules` - Cursor IDE settings

### Documentation

- `README.md` - Main project overview
- `docs/` - Detailed guides and documentation
- `CLEANUP_SUMMARY.md` - Cleanup process documentation

## 🔄 Version Control

### Git Ignore Patterns

The project includes appropriate `.gitignore` patterns for:

- Python cache files
- Virtual environments
- Log files
- Temporary files
- IDE-specific files

### Commit Guidelines

- Keep commits focused and descriptive
- Update documentation when adding features
- Run cleanup script before major commits

## 🎯 Best Practices

1. **Organization First**: Always place files in appropriate directories
2. **Documentation**: Keep docs updated with code changes
3. **Cleanliness**: Run cleanup script regularly
4. **Consistency**: Follow established naming conventions
5. **Maintenance**: Address technical debt promptly

## 🆘 Troubleshooting

### Common Issues

- **Missing directories**: Run cleanup script to recreate structure
- **File conflicts**: Check if files are in correct locations
- **Docker issues**: Verify docker-compose.yml configuration

### Getting Help

- Check `docs/` directory for relevant guides
- Review `CLEANUP_SUMMARY.md` for recent changes
- Run cleanup script to restore organization

---

_This guide helps maintain the clean, organized structure of the Memory Context Manager v2 project._
