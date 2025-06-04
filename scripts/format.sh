#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running isort...${NC}"
isort .

echo -e "${GREEN}Running black...${NC}"
black .

echo -e "${GREEN}Formatting complete!${NC}"