# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

md2conf is a Python package that parses Markdown files, converts them to Confluence Storage Format (XHTML), and uploads them to Confluence wiki via API endpoints. The tool supports both single-page and directory-mode publishing with features like image handling, LaTeX formulas, Mermaid diagrams, draw.io integration, and comprehensive Markdown-to-Confluence conversion.

## Development Commands

### Setup Environment
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Alternative with standard Python
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Code Quality & Testing
```bash
# Run all static checks, formatting, and type checking
./check.sh          # Linux/macOS
check.bat           # Windows

# Individual commands (using uv):
uv run ruff check                       # Linting
uv run ruff format --check             # Format checking
uv run ruff format                      # Auto-format code
uv run mypy md2conf                     # Type check main package
uv run mypy tests                       # Type check tests
uv run mypy integration_tests           # Type check integration tests

# Run unit tests
uv run python -m unittest discover -s tests

# Run integration tests (requires Confluence environment setup)
uv run python -m unittest discover -s integration_tests

# Test help message
uv run python -m md2conf --help

# Generate documentation
uv run python documentation.py

# Alternative with standard Python:
python -m ruff check
python -m mypy md2conf
python -m unittest discover -s tests
```

### Building & Packaging
```bash
# Build and test package with Docker
./package.sh

# Individual build steps:
uv run python -m build --sdist --wheel  # Create PyPI package (using uv)
python -m build --sdist --wheel         # Alternative with standard Python
```

## Architecture Overview

### Core Components

- **`__main__.py`**: Entry point with argument parsing and main execution flow
- **`api.py`**: Confluence REST API client handling authentication and HTTP operations  
- **`converter.py`**: Main conversion engine from Markdown to Confluence Storage Format
- **`processor.py`**: File processing pipeline coordinating conversion steps
- **`publisher.py`**: Handles uploading content and attachments to Confluence
- **`scanner.py`**: Directory traversal and file discovery with `.mdignore` support
- **`matcher.py`**: URL resolution and link handling for directory mode

### Specialized Modules

- **`drawio.py`**: draw.io diagram processing and conversion
- **`mermaid.py`**: Mermaid diagram rendering via mermaid-cli
- **`latex.py`**: LaTeX formula rendering using matplotlib
- **`markdown.py`**: Markdown parsing configuration and extensions
- **`csf.py`**: Confluence Storage Format XML utilities
- **`xml.py`**: XML parsing and manipulation helpers
- **`metadata.py`**: Front-matter parsing (YAML/JSON)
- **`environment.py`**: Configuration management from env vars and CLI args

### Data Models

- **`domain.py`**: Core data structures and type definitions
- **`collection.py`**: Document collection management
- **`local.py`**: Local file output mode implementation

## Code Conventions

- **Type Hints**: Strict typing enforced via mypy with comprehensive type annotations
- **Error Handling**: Proper exception handling with informative error messages
- **Logging**: Structured logging throughout with appropriate log levels
- **Code Style**: Ruff formatting with line length 160, strict linting rules (E, F, B, I, Q)
- **Testing**: Comprehensive unit tests in `tests/`, integration tests in `integration_tests/`
- **Documentation**: Docstrings required for all public methods, classes, and functions

## Testing Strategy

### Unit Tests (`tests/`)
- `test_conversion.py`: Core Markdown to CSF conversion testing
- `test_xml.py`: XML parsing and manipulation
- `test_processor.py`: File processing pipeline
- `test_scanner.py`: Directory scanning and file discovery
- `test_matcher.py`: URL resolution and link handling
- `test_drawio.py`, `test_mermaid.py`: Diagram processing
- `test_unit.py`: Additional unit tests

### Integration Tests (`integration_tests/`)
- Requires live Confluence instance with environment variables configured
- Tests end-to-end publishing workflow

## Environment Configuration

The application supports configuration via environment variables:
- `CONFLUENCE_DOMAIN`: Confluence domain (e.g., example.atlassian.net)
- `CONFLUENCE_PATH`: Base path (typically /wiki/)  
- `CONFLUENCE_USER_NAME`: Username for basic auth
- `CONFLUENCE_API_KEY`: API token
- `CONFLUENCE_SPACE_KEY`: Target space key
- `CONFLUENCE_API_URL`: Direct API URL for scoped tokens

## Key Features Implementation

- **Directory Mode**: Hierarchical publishing with parent-child relationships via `index.md`/`README.md`
- **Image Handling**: Automatic upload as attachments with SVG→PNG fallback
- **Diagram Support**: draw.io and Mermaid with render/no-render options
- **Math Formulas**: LaTeX rendering via matplotlib or marketplace app
- **Front-matter**: YAML/JSON metadata for titles, tags, properties
- **Link Resolution**: Relative links converted to Confluence URLs in directory mode
- **Confluence Widgets**: Status labels, TOC, date widgets, custom CSF blocks