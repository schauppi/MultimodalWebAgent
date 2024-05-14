
#!/bin/bash

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
export PATH="$HOME/.local/bin:$PATH"

# Install SQLite dependencies
apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Install dependencies using Poetry
poetry install

# Run the webagent
poetry run webagent
