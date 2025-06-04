#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running isort...${NC}"
isort . --check-only --diff

echo -e "${GREEN}Running black...${NC}"
black . --check --diff

echo -e "${GREEN}Running flake8...${NC}"
flake8 .

echo -e "${GREEN}Running mypy...${NC}"
mypy src/aem_admin_client

echo -e "${GREEN}All linting checks passed!${NC}"