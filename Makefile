.PHONY: install test lint format clean dev-install run-examples

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
	ruff check mcp_base/
	mypy mcp_base/

# Format code
format:
	black mcp_base/ tests/ examples/
	isort mcp_base/ tests/ examples/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Run example servers
run-minimal:
	python examples/minimal_server.py

run-auth:
	python examples/auth_patterns.py

run-advanced:
	python examples/advanced_patterns.py

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
	@echo "  run-minimal  - Run minimal example server"
	@echo "  run-auth     - Run auth patterns example"
	@echo "  run-advanced - Run advanced patterns example"
	@echo "  build        - Build package"
	@echo "  help         - Show this help"