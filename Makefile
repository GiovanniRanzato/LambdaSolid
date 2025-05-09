# Load .env variables
include .env
export $(shell sed 's/=.*//' .env)

# Define ANSI color codes
GREEN  = \033[0;32m
YELLOW = \033[0;33m
NC     = \033[0m

# Python virtual environment setup
create_venv:
	python3.13 -m venv venv

activate_venv:
	source venv/bin/activate

install_setup_tools:
	python -m ensurepip --upgrade
	python -m pip install --upgrade pip setuptools

# Install dependencies
install:
	pip install --upgrade pip && \
 	pip install -r layer/requirements.txt && \
 	pip install -r tests/requirements.txt

.PHONY: new_dependency
.PHONY: new_test_dependency
new_dependency:
	@read -p "Dependency name: " pkg; \
	pip install $$pkg && \
	pip show $$pkg | grep Version | awk '{print "'$$pkg'==" $$2}' >> layer/requirements.txt && \
	echo "$$pkg added to  layer/requirements.txt"

new_test_dependency:
	@read -p "Test dependency name: " pkg; \
	pip install $$pkg && \
	pip show $$pkg | grep Version | awk '{print "'$$pkg'==" $$2}' >> tests/requirements.txt && \
	echo "$$pkg added to  tests/requirements.txt"


# Linting
lint:
	ruff check src && ruff check tests

# Format code
format:
	ruff format src && ruff format tests

# Run tests
test:
	pytest tests/unit -n 3 -v --cov=src --cov-report=term-missing --cov-fail-under=99

integration:
	pytest tests/integration -v || pytest --last-failed -v

# Pre-commit hooks
pre-commit:
	@echo "$(YELLOW)Running pre-commit tasks...$(NC)"
	@make format
	@make test
	@make integration
	@echo "$(GREEN)Pre-commit tasks: OK$(NC)"

# Generate coverage report
coverage:
	pytest tests/unit -n 3 --cov=src --cov-report=html --cov-config=.coveragerc && \
	if [ "$$(uname)" = "Darwin" ]; then \
		open htmlcov/index.html; \
	elif [ "$$(uname)" = "Windows" ]; then \
		start htmlcov\\index.html; \
	fi

localstack:
	docker stop localstack || true
	docker rm localstack || true
	docker run -d -p 4566:4566 --name localstack -it localstack/localstack

	#Create AWS local resources
	chmod +x ./localstack-resources.sh
	./localstack-resources.sh


dynamodb:
	AWS_REGION=$(DYNAMODB_REGION) DYNAMO_ENDPOINT=$(DYNAMODB_ENDPOINT) dynamodb-admin