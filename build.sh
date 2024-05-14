#!/bin/bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install dependencies using Poetry
poetry install

# Run the webagent
poetry run webagent
