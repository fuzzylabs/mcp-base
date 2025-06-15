.PHONY: install test lint format clean dev-install

# Install package
install:
	pip install -e .

# Install with development dependencies
dev-install:
	pip install -e ".[dev]"

# Run tests
test:
	pytest

# Run linting
lint:
	ruff check mcp_server_toolkit/
	mypy mcp_server_toolkit/

# Format code
format:
	black mcp_server_toolkit/ tests/ examples/
	isort mcp_server_toolkit/ tests/ examples/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run example Capsule server
run-capsule:
	python examples/capsule_server.py

# Run example Capsule server in stdio mode
run-capsule-stdio:
	python examples/capsule_server.py stdio

# Build package
build:
	python -m build

# Help
help:
	@echo "Available commands:"
	@echo "  install      - Install package"
	@echo "  dev-install  - Install with development dependencies"
	@echo "  test         - Run tests"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code"
	@echo "  clean        - Clean build artifacts"
	@echo "  run-capsule  - Run example Capsule server"
	@echo "  run-capsule-stdio - Run Capsule server in stdio mode"
	@echo "  build        - Build package"
	@echo "  help         - Show this help"