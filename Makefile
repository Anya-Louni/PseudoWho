# Makefile for PseudoQui Project
# Simplifies setup, running, and testing the application

# Color output
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[0;33m
NC=\033[0m # No Color

# Python
PYTHON=python
PIP=pip
BACKEND_DIR=backend
BACKEND_ENTRY=run.py

# Node/React
NPM=npm
FRONTEND_DIR=frontend

# Pytest
PYTEST=pytest

.PHONY: help install install-backend install-frontend run run-backend run-frontend test clean dev setup

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Complete project setup (install all dependencies)
	@echo "$(GREEN)Setting up PseudoQui project...$(NC)"
	@$(PYTHON) setup.py

install: install-backend install-frontend ## Install all dependencies

install-backend: ## Install Python dependencies
	@echo "$(GREEN)Installing backend dependencies...$(NC)"
	cd $(BACKEND_DIR) && $(PIP) install -r requirements.txt
	@echo "$(GREEN)Backend dependencies installed$(NC)"

install-frontend: ## Install Node dependencies
	@echo "$(GREEN)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) install
	@echo "$(GREEN)Frontend dependencies installed$(NC)"

run: ## Run both frontend and backend (requires 2 terminals)
	@echo "$(YELLOW)Note: Run 'make run-backend' in one terminal and 'make run-frontend' in another$(NC)"

run-backend: ## Run backend server
	@echo "$(GREEN)Starting backend server on http://localhost:5000$(NC)"
	cd $(BACKEND_DIR) && $(PYTHON) $(BACKEND_ENTRY)

run-frontend: ## Run frontend development server
	@echo "$(GREEN)Starting frontend server on http://localhost:3000$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) start

test: ## Run backend tests
	@echo "$(GREEN)Running tests...$(NC)"
	cd $(BACKEND_DIR) && $(PYTHON) -m $(PYTEST) tests/ -v

test-coverage: ## Run tests with coverage report
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	cd $(BACKEND_DIR) && $(PYTHON) -m pytest tests/ --cov=app --cov-report=html
	@echo "$(GREEN)Coverage report generated in backend/htmlcov/index.html$(NC)"

clean: ## Clean generated files and caches
	@echo "$(YELLOW)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf $(BACKEND_DIR)/data/tree_data.json 2>/dev/null || true
	rm -rf $(BACKEND_DIR)/data/game_history.json 2>/dev/null || true
	rm -rf $(FRONTEND_DIR)/build 2>/dev/null || true
	rm -rf $(FRONTEND_DIR)/node_modules 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete$(NC)"

clean-data: ## Clean only data files (tree and history)
	@echo "$(YELLOW)Cleaning data files...$(NC)"
	rm -f $(BACKEND_DIR)/data/tree_data.json
	rm -f $(BACKEND_DIR)/data/game_history.json
	@echo "$(GREEN)Data files cleaned$(NC)"

dev: install ## Setup development environment
	@echo "$(GREEN)Development environment ready!$(NC)"
	@echo "Run '$(YELLOW)make run-backend$(NC)' in one terminal"
	@echo "Run '$(YELLOW)make run-frontend$(NC)' in another terminal"

build-frontend: ## Build frontend for production
	@echo "$(GREEN)Building frontend...$(NC)"
	cd $(FRONTEND_DIR) && $(NPM) run build
	@echo "$(GREEN)Frontend built to $(FRONTEND_DIR)/build$(NC)"

lint: ## Lint Python code (requires flake8)
	@echo "$(GREEN)Linting Python code...$(NC)"
	cd $(BACKEND_DIR) && $(PYTHON) -m flake8 app/ --max-line-length=120 --exclude=__pycache__

format: ## Format Python code (requires black)
	@echo "$(GREEN)Formatting Python code...$(NC)"
	cd $(BACKEND_DIR) && $(PYTHON) -m black app/ tests/

check: test lint ## Run all checks (tests + linting)
	@echo "$(GREEN)All checks passed!$(NC)"

status: ## Show project status
	@echo "$(GREEN)PseudoQui Project Status$(NC)"
	@echo "Backend: $(BACKEND_DIR)"
	@echo "Frontend: $(FRONTEND_DIR)"
	@echo ""
	@echo "Python version:"
	@$(PYTHON) --version
	@echo ""
	@echo "Node version:"
	@node --version
	@echo ""
	@echo "npm version:"
	@$(NPM) --version

.DEFAULT_GOAL := help
